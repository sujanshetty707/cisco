#!/usr/bin/env python3
"""
myanswers - Private CLI client for Data Communication & Computer Network Lab experiments.
Retrieves and updates experiment answers stored in a private GitHub repository.

Zero external dependencies - uses Python standard library only.
"""

import sys
import os
import json
import base64
import argparse
import subprocess
import tempfile
import urllib.request
import urllib.error
import socket
from pathlib import Path

# Ensure UTF-8 output where possible on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# --- Configuration Constants ---
DEFAULT_REPO = "sujanshetty707/cisco"
DEFAULT_BRANCH = "main"
CONFIG_DIR = Path.home() / ".myanswers"
CONFIG_FILE = CONFIG_DIR / "config.json"

EXPERIMENTS = {
    1: "Basic Network Commands and Network Devices",
    2: "Basic Configuration of Switch/Router Using Cisco Packet Tracer",
    3: "Configure Privilege Level Password and User Authentication in Switch",
    4: "Configure DHCP Server and Wireless Router and Check Connectivity",
    5: "Configure Static Routing Using Cisco Packet Tracer",
}

DIVIDER = "=" * 65
LINE = "-" * 65


def get_token() -> str:
    """Retrieve GitHub token from environment or local config."""
    # 1. Environment variable (highest priority)
    env_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("MYANSWERS_TOKEN")
    if env_token and env_token.strip():
        return env_token.strip()

    # 2. Local user config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                token = data.get("token")
                if token and token.strip():
                    return token.strip()
        except Exception:
            pass

    return ""


def prompt_for_token() -> str:
    """Interactively prompt user for GitHub token without echoing characters."""
    import getpass

    print("\nGitHub Personal Access Token not detected.")
    print("A token is required to access your private repository.")
    print("Scopes required: 'repo' (Full control of private repositories)\n")

    token = getpass.getpass("Enter your GitHub Personal Access Token (hidden): ").strip()
    if not token:
        print("Error: Token cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Offer to save locally
    save_choice = input("Save token locally for future one-command usage? (y/N): ").strip().lower()
    if save_choice in ("y", "yes"):
        save_config(token=token)
        print("[OK] Token saved to ~/.myanswers/config.json\n")
    else:
        print("Tip: You can export GITHUB_TOKEN=<your_token> in your shell profile.\n")

    return token


def get_repo() -> str:
    """Retrieve target GitHub repository name (owner/repo)."""
    env_repo = os.environ.get("MYANSWERS_REPO")
    if env_repo and env_repo.strip():
        return env_repo.strip()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                repo = data.get("repo")
                if repo and repo.strip():
                    return repo.strip()
        except Exception:
            pass

    return DEFAULT_REPO


def save_config(token: str = None, repo: str = None, branch: str = None):
    """Save configuration to ~/.myanswers/config.json with restricted permissions."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    current = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                current = json.load(f)
        except Exception:
            current = {}

    if token is not None:
        current["token"] = token
    if repo is not None:
        current["repo"] = repo
    elif "repo" not in current:
        current["repo"] = DEFAULT_REPO

    if branch is not None:
        current["branch"] = branch
    elif "branch" not in current:
        current["branch"] = DEFAULT_BRANCH

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)

    # Set restricted permissions on Unix/macOS
    try:
        if os.name != "nt":
            os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass


def mask_token(token: str) -> str:
    """Mask token for display purposes."""
    if not token:
        return "<not set>"
    if len(token) <= 8:
        return "*" * len(token)
    return token[:4] + "*" * (len(token) - 8) + token[-4:]


# --- GitHub Operations ---

def fetch_raw_content(repo: str, path: str) -> str | None:
    """Fetch raw text directly from public GitHub URL without any token."""
    for branch in [DEFAULT_BRANCH, "master"]:
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "myanswers-cli"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception:
            continue
    return None


def make_api_request(url: str, token: str = None, method: str = "GET", data: bytes = None) -> dict:
    """Execute an HTTP request to the GitHub REST API using urllib."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "myanswers-cli",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as err:
        if err.code in (401, 403):
            raise PermissionError(
                f"GitHub access error (HTTP {err.code}).\n"
                "If the repository requires authentication, ensure your token is valid with 'repo' scope.\n"
                "To configure a token, run: myanswers config --token <your_token>"
            )
        elif err.code == 404:
            raise FileNotFoundError(f"File or repository not found on GitHub (HTTP 404): {url}")
        else:
            try:
                err_json = json.loads(err.read().decode("utf-8"))
                msg = err_json.get("message", str(err))
            except Exception:
                msg = str(err)
            raise RuntimeError(f"GitHub API Error (HTTP {err.code}): {msg}")
    except (urllib.error.URLError, socket.timeout, ConnectionError) as err:
        raise ConnectionError(
            "Unable to connect to GitHub.\n"
            "Please check your internet connection and network settings."
        )


def fetch_experiment(exp_num: int, repo: str, token: str = None) -> tuple[str, str, str]:
    """
    Fetch ONLY the specified experiment file from GitHub.
    Returns: (content_text, blob_sha, matched_path)
    """
    candidate_paths = [
        f"experiments/exp{exp_num}.txt",
        f"lab-answers/experiments/exp{exp_num}.txt",
        f"exp{exp_num}.txt",
    ]

    # Fast path: Try fetching raw content (works without token on public repo)
    for path in candidate_paths:
        raw_text = fetch_raw_content(repo, path)
        if raw_text is not None:
            return raw_text, "", path

    # Fallback to GitHub REST API
    last_error = None
    for path in candidate_paths:
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        try:
            data = make_api_request(url, token)
            content_encoded = data.get("content", "")
            sha = data.get("sha", "")
            raw_bytes = base64.b64decode(content_encoded)
            content_text = raw_bytes.decode("utf-8", errors="replace")
            return content_text, sha, path
        except FileNotFoundError as e:
            last_error = e
            continue

    if last_error:
        raise last_error
    raise FileNotFoundError(f"Experiment {exp_num} file not found in repository {repo}.")


def push_experiment_update(exp_num: int, new_content: str, repo: str, token: str, sha: str, path: str = None) -> dict:
    """Commit and push updated experiment content to GitHub."""
    target_path = path or f"experiments/exp{exp_num}.txt"
    url = f"https://api.github.com/repos/{repo}/contents/{target_path}"

    b64_content = base64.b64encode(new_content.encode("utf-8")).decode("ascii")
    payload = {
        "message": f"Update exp{exp_num}.txt via myanswers",
        "content": b64_content,
        "sha": sha,
    }

    data_bytes = json.dumps(payload).encode("utf-8")
    return make_api_request(url, token, method="PUT", data=data_bytes)


# --- Display Functions ---

def display_experiment_content(exp_num: int, content: str):
    """Cleanly display ONLY the selected experiment."""
    title = EXPERIMENTS.get(exp_num, f"Experiment {exp_num}")
    print()
    print(DIVIDER)
    print(f" EXPERIMENT {exp_num}: {title.upper()}")
    print(DIVIDER)
    print()
    print(content.strip())
    print()
    print(DIVIDER)


def display_menu():
    """Display the experiment selection menu."""
    print()
    print("MY LAB EXPERIMENTS")
    print()
    for num in range(1, 6):
        print(f"[{num}] Experiment {num}")
    print()


def show_offline_fallback(exp_num: int) -> bool:
    """Check if local copy exists in current directory or experiments/."""
    candidates = [
        Path(f"experiments/exp{exp_num}.txt"),
        Path(f"lab-answers/experiments/exp{exp_num}.txt"),
        Path(f"exp{exp_num}.txt"),
    ]
    for c in candidates:
        if c.exists():
            try:
                text = c.read_text(encoding="utf-8")
                print(f"\n[OFFLINE FALLBACK] Showing local cached file: {c}")
                display_experiment_content(exp_num, text)
                return True
            except Exception:
                pass
    return False


def view_experiment(exp_num: int, repo: str, token: str):
    """Download and display ONLY the selected experiment."""
    if exp_num not in EXPERIMENTS:
        print(f"Error: Invalid experiment number '{exp_num}'. Please enter 1-5.", file=sys.stderr)
        return

    try:
        print(f"\nConnecting to GitHub ({repo})... Fetching Experiment {exp_num}...")
        content, _, _ = fetch_experiment(exp_num, repo, token)
        display_experiment_content(exp_num, content)
    except PermissionError as err:
        print(f"\n[AUTHENTICATION ERROR]\n{err}", file=sys.stderr)
    except ConnectionError as err:
        print(f"\n[NETWORK ERROR]\n{err}", file=sys.stderr)
        show_offline_fallback(exp_num)
    except FileNotFoundError as err:
        print(f"\n[FILE NOT FOUND]\n{err}", file=sys.stderr)
        show_offline_fallback(exp_num)
    except Exception as err:
        print(f"\n[ERROR]\n{err}", file=sys.stderr)


# --- Update Workflow ---

def open_in_system_editor(initial_content: str, exp_num: int) -> str | None:
    """Open a temporary file in the user's default text editor and return the updated text."""
    with tempfile.NamedTemporaryFile("w+", suffix=f"_exp{exp_num}.txt", delete=False, encoding="utf-8") as tf:
        tf.write(initial_content)
        temp_path = tf.name

    try:
        # Determine editor command
        editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
        if not editor:
            if os.name == "nt":
                editor = "notepad.exe"
            else:
                editor = "nano" if subprocess.call(["which", "nano"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else "vi"

        print(f"Opening Experiment {exp_num} in editor ({editor})...")
        print("Save and close the editor when you are done.\n")
        ret = subprocess.call([editor, temp_path])
        if ret != 0:
            print("Editor exited with an error code.", file=sys.stderr)
            return None

        with open(temp_path, "r", encoding="utf-8") as f:
            new_content = f.read()

        return new_content
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass


def handle_update(exp_num: int, file_path: str = None):
    """Handle updating an experiment answer on GitHub."""
    if exp_num not in EXPERIMENTS:
        print(f"Error: Invalid experiment number '{exp_num}'. Please select 1 to 5.", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    if not token:
        token = prompt_for_token()

    repo = get_repo()

    print(f"Fetching current Experiment {exp_num} from {repo}...")
    try:
        current_content, sha, path = fetch_experiment(exp_num, repo, token)
    except FileNotFoundError:
        # File doesn't exist yet on remote
        current_content = ""
        sha = ""
        path = f"experiments/exp{exp_num}.txt"
    except Exception as e:
        print(f"Error fetching experiment from GitHub: {e}", file=sys.stderr)
        sys.exit(1)

    # Obtain new content
    if file_path:
        local_p = Path(file_path)
        if not local_p.exists():
            print(f"Error: Local file '{file_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
        new_content = local_p.read_text(encoding="utf-8")
    else:
        new_content = open_in_system_editor(current_content, exp_num)
        if new_content is None:
            print("Update cancelled.")
            return

    if new_content.strip() == current_content.strip():
        print("No changes detected. Update cancelled.")
        return

    print()
    print(LINE)
    print(f" Ready to commit and push changes for Experiment {exp_num}")
    print(f" Target Repository: {repo}")
    print(f" Target File:       {path}")
    print(LINE)
    confirm = input("Push this new version to GitHub? (y/N): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("Update cancelled by user.")
        return

    try:
        print("Pushing updated experiment to GitHub...")
        push_experiment_update(exp_num, new_content, repo, token, sha, path)
        print(f"\n[OK] Successfully updated Experiment {exp_num} on GitHub!")
    except Exception as e:
        print(f"\nError pushing update to GitHub: {e}", file=sys.stderr)
        sys.exit(1)


# --- Config Management ---

def handle_config(args):
    """Handle configuration inspection and updates."""
    if args.token:
        save_config(token=args.token)
        print("[OK] GitHub token updated.")
    if args.repo:
        save_config(repo=args.repo)
        print(f"[OK] Target repository set to '{args.repo}'.")

    if not args.token and not args.repo:
        token = get_token()
        repo = get_repo()
        print("\n--- Current Configuration ---")
        print(f"Repository:  {repo}")
        print(f"Token:       {mask_token(token)}")
        print(f"Config File: {CONFIG_FILE}")
        if not token:
            print("\nNo token configured.")
            print("To set your token, run:")
            print("  myanswers config --token <your_github_token>")
            print("Or set the environment variable:")
            print("  export GITHUB_TOKEN=<your_github_token>   (Linux/macOS)")
            print("  $env:GITHUB_TOKEN=\"<your_github_token>\"   (PowerShell)")


def handle_logout():
    """Clear saved token from local config file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.pop("token", None)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("[OK] Saved GitHub token has been cleared.")
        except Exception as e:
            print(f"Error clearing config: {e}", file=sys.stderr)
    else:
        print("No configuration file found.")


# --- Interactive Menu Loop ---

def interactive_menu(repo: str, token: str):
    """Run the interactive menu loop."""
    display_menu()

    while True:
        try:
            choice = input("Enter experiment number: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if choice in ("0", "exit", "quit", "q"):
            print("Exiting.")
            break

        if choice.isdigit() and 1 <= int(choice) <= 5:
            exp_num = int(choice)
            view_experiment(exp_num, repo, token)
            print("\nEnter experiment number (1-5 to view another, 0 to exit): ", end="")
            while True:
                try:
                    next_choice = input().strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nExiting.")
                    return

                if next_choice in ("0", "exit", "quit", "q"):
                    print("Exiting.")
                    return
                elif next_choice.isdigit() and 1 <= int(next_choice) <= 5:
                    exp_num = int(next_choice)
                    view_experiment(exp_num, repo, token)
                    print("\nEnter experiment number (1-5 to view another, 0 to exit): ", end="")
                else:
                    print("Invalid choice. Please enter 1-5 to view an experiment or 0 to exit: ", end="")
        else:
            print("Invalid experiment number. Please select a number between 1 and 5 (or 0 to exit).\n")


# --- Main Entry Point ---

def main():
    parser = argparse.ArgumentParser(
        prog="myanswers",
        description="Command-line tool to view and update private lab experiment answers.",
        add_help=False,
    )

    # Subcommands and direct argument handling
    subparsers = parser.add_subparsers(dest="command")

    # update subcommand
    update_parser = subparsers.add_parser("update", help="Update an experiment and push to GitHub")
    update_parser.add_argument("number", type=int, help="Experiment number (1-5)")
    update_parser.add_argument("file", nargs="?", default=None, help="Optional local file to upload")

    # config subcommand
    config_parser = subparsers.add_parser("config", help="View or update local configuration")
    config_parser.add_argument("--token", help="Set GitHub Personal Access Token")
    config_parser.add_argument("--repo", help="Set target repository (e.g. sujanshetty707/cisco)")

    # logout subcommand
    subparsers.add_parser("logout", help="Remove saved token from local config")

    # help subcommand
    subparsers.add_parser("help", help="Show help message")

    # Check for direct integer invocation, e.g. "myanswers 3" or help flags
    argv = sys.argv[1:]
    if argv and argv[0] in ("-h", "--help", "help"):
        print("Usage:")
        print("  myanswers               Open interactive experiment menu")
        print("  myanswers <1-5>         Directly display a specific experiment (e.g. 'myanswers 3')")
        print("  myanswers update <1-5>  Edit an experiment and push changes to GitHub")
        print("  myanswers update <1-5> <file.txt>  Upload a local file as an experiment")
        print("  myanswers config        View or update stored credentials/repository")
        print("  myanswers logout        Remove locally saved GitHub token")
        return

    # Direct experiment number check, e.g., "myanswers 3"
    if argv and len(argv) == 1 and argv[0].isdigit():
        exp_num = int(argv[0])
        if 1 <= exp_num <= 5:
            token = get_token()
            repo = get_repo()
            view_experiment(exp_num, repo, token)
            return
        else:
            print(f"Error: Invalid experiment number '{exp_num}'. Please select 1 to 5.", file=sys.stderr)
            sys.exit(1)

    args = parser.parse_args(argv)

    if args.command == "update":
        handle_update(args.number, args.file)
    elif args.command == "config":
        handle_config(args)
    elif args.command == "logout":
        handle_logout()
    elif args.command is None:
        # Default interactive menu
        token = get_token()
        repo = get_repo()
        interactive_menu(repo, token)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

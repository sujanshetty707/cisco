# Terminal Roadmap: Getting Answers on Another PC

This roadmap is designed for **pure terminal usage** (Command Prompt, PowerShell, or Bash). You do **not** need to run any Python package managers or pip commands.

---

## What You Need
1. Your **GitHub Personal Access Token** (the `ghp_...` token with `repo` permission).
2. A terminal (Command Prompt, PowerShell, or Bash).

---

## Step 1: Open Terminal and Get the Folder

### Option A: If Git is installed
```bash
git clone https://github.com/sujanshetty707/cisco.git
cd cisco
```

### Option B: If Git is NOT installed

Choose any of these quick methods:

* **Method 1 (Directly in Terminal with `curl` - Built into Windows 10/11 & Mac/Linux):**
  Run these two commands in your terminal (paste your token in place of `YOUR_TOKEN`):
  ```cmd
  curl -H "Authorization: token YOUR_TOKEN" -H "Accept: application/vnd.github.v3.raw" -L -o myanswers.py https://api.github.com/repos/sujanshetty707/cisco/contents/myanswers.py
  curl -H "Authorization: token YOUR_TOKEN" -H "Accept: application/vnd.github.v3.raw" -L -o myanswers.bat https://api.github.com/repos/sujanshetty707/cisco/contents/myanswers.bat
  ```

* **Method 2 (USB Flash Drive - Easiest & Fastest for Labs):**
  Keep just two files (`myanswers.bat` and `myanswers.py`) on a USB stick.  
  Plug it into the PC, open the terminal in your USB drive, and you are ready.

* **Method 3 (Browser Download):**
  Open your browser, go to `https://github.com/sujanshetty707/cisco`, click **<> Code** -> **Download ZIP**, extract the folder, and open terminal there.

---

## Step 2: Enable the `myanswers` Command

Run this **one command** in your terminal so you can type `myanswers` from anywhere:

* **In PowerShell (Windows):**
  ```powershell
  $env:Path += ";$PWD"
  ```

* **In Command Prompt / CMD (Windows):**
  ```cmd
  set PATH=%PATH%;%cd%
  ```

* **In Linux / macOS Terminal:**
  ```bash
  export PATH="$PATH:$PWD"
  ```

*(Now `myanswers` is an active terminal command in your session).*

---

## Step 3: Link Your GitHub Token (Run Once)

In your terminal, run:

```cmd
myanswers config --token ghp_YOUR_GITHUB_TOKEN_HERE
```
*(Replace `ghp_YOUR_GITHUB_TOKEN_HERE` with your actual token).*

Output:
```text
[OK] GitHub token updated.
```

> **Security Note:** The token is saved in your local user profile (`~/.myanswers/config.json`) and is never printed on screen.

---

## Step 4: Get Your Answers

### Method 1: Open the Menu
Just type:
```cmd
myanswers
```

Output:
```text
MY LAB EXPERIMENTS

[1] Experiment 1
[2] Experiment 2
[3] Experiment 3
[4] Experiment 4
[5] Experiment 5

Enter experiment number: 3
```
* Enter `3` to fetch and view **only** Experiment 3.
* Afterwards, type another number `1-5` to view another experiment, or `0` to exit.

---

### Method 2: View an Experiment Directly (Fastest)
You can directly pass the experiment number:

* To view Experiment 1:
  ```cmd
  myanswers 1
  ```
* To view Experiment 2:
  ```cmd
  myanswers 2
  ```
* To view Experiment 3:
  ```cmd
  myanswers 3
  ```
* To view Experiment 4:
  ```cmd
  myanswers 4
  ```
* To view Experiment 5:
  ```cmd
  myanswers 5
  ```

---

## Step 5: Clean Up When Leaving the PC

When you are done using a shared or college lab PC, erase your saved token with one command:

```cmd
myanswers logout
```

Output:
```text
[OK] Saved GitHub token has been cleared.
```

---

## 5-Second Cheat Sheet

```cmd
cd cisco
myanswers config --token <your_token>
myanswers 3
myanswers logout
```

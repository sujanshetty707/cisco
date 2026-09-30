# Quick Roadmap: Getting Lab Answers on Another PC

Follow these simple steps whenever you are sitting at another computer (such as a college lab PC or laptop) and need to retrieve your experiment answers.

---

## Prerequisites (What You Need)
1. **Python 3** installed on the PC (standard on most systems).
2. Your **GitHub Personal Access Token** (the `ghp_...` token with `repo` permission).
3. Internet connection.

---

## Step 1: Get the Client Script on the PC

Choose **either** Method A or Method B:

### Method A: Single File (Fastest – No Git Required)
Download or copy just **`myanswers.py`** to the PC:
* Using PowerShell / Command Prompt:
  ```powershell
  curl -O https://raw.githubusercontent.com/sujanshetty707/cisco/main/myanswers.py
  ```
* *Or simply transfer `myanswers.py` via a USB drive / email / Google Drive.*

### Method B: Clone the Repository (If Git is installed)
```bash
git clone https://github.com/sujanshetty707/cisco.git
cd cisco
```

---

## Step 2: Set Up the "myanswers" Command

To make it callable by typing just `myanswers`:

* **On Windows (PowerShell or CMD):**
  In the folder where `myanswers.py` is located, run:
  ```powershell
  python -m pip install -e .
  ```
  *(Or if using standalone file without pip, simply run: `python myanswers.py`)*

* **On Linux / macOS:**
  ```bash
  python3 -m pip install -e .
  ```

---

## Step 3: Enter Your GitHub Token (One-Time Setup)

Run this command once to link your private GitHub repository:

```cmd
myanswers config --token ghp_YOUR_GITHUB_TOKEN_HERE
```
*(Replace `ghp_YOUR_GITHUB_TOKEN_HERE` with your actual token).*

> **Note:** The token is securely stored in your user profile (`~/.myanswers/config.json`) and masked so it is never displayed on screen.

---

## Step 4: Get Your Answers

### Option 1: Interactive Menu
Run:
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
Type any number (`1` to `5`) and press **Enter**.
* Only the chosen experiment is downloaded and shown.
* Afterward, type another number (`1-5`) to view another experiment, or `0` to exit.

---

### Option 2: Direct Command (Instant View)
To view a specific experiment directly without opening the menu:

* To view Experiment 1:
  ```cmd
  myanswers 1
  ```
* To view Experiment 3:
  ```cmd
  myanswers 3
  ```
* To view Experiment 5:
  ```cmd
  myanswers 5
  ```

---

## Step 5: Clean Up When Done (Crucial for Shared/Lab PCs)

When you finish using a public or shared college lab PC, erase your token so nobody else can access your answers:

```cmd
myanswers logout
```
Output:
```text
[OK] Saved GitHub token has been cleared.
```

---

## Summary Cheat Sheet

| Task | Command |
|:---|:---|
| Set up token | `myanswers config --token <your_token>` |
| Open interactive menu | `myanswers` |
| View Experiment 3 directly | `myanswers 3` |
| Log out / delete token from PC | `myanswers logout` |

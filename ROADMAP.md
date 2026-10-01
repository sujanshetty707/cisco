# Terminal Roadmap: Getting Answers on Another PC (Public Repo - No Token Required)

The repository is **PUBLIC**. You do **NOT** need any GitHub Personal Access Token, login, or Python package installation to retrieve answers on any PC.

---

## Method 1: Using the `myanswers` Command (Recommended)

### Step 1: Open Terminal & Clone or Download
* **If Git is installed:**
  ```bash
  git clone https://github.com/sujanshetty707/cisco.git
  cd cisco
  ```

* **If Git is NOT installed (Download via terminal):**
  * **In PowerShell:**
    ```powershell
    curl.exe -O https://raw.githubusercontent.com/sujanshetty707/cisco/main/myanswers.bat
    curl.exe -O https://raw.githubusercontent.com/sujanshetty707/cisco/main/myanswers.py
    ```
    *(Note: You must type `curl.exe` instead of `curl` in PowerShell because PowerShell aliases `curl` to `Invoke-WebRequest`)*.

  * **In Command Prompt (CMD):**
    ```cmd
    curl -O https://raw.githubusercontent.com/sujanshetty707/cisco/main/myanswers.bat
    curl -O https://raw.githubusercontent.com/sujanshetty707/cisco/main/myanswers.py
    ```

* **Or use a USB Flash Drive:**
  Keep `myanswers.bat` and `myanswers.py` on your USB stick. Plug it in and open terminal in that folder.

---

### Step 2: Get Answers (Zero Setup, No Token Needed!)

#### Option A: Direct View (Fastest)
Pass the experiment number directly:

* **Experiment 1:**
  ```cmd
  myanswers 1
  ```
* **Experiment 2:**
  ```cmd
  myanswers 2
  ```
* **Experiment 3:**
  ```cmd
  myanswers 3
  ```
* **Experiment 4:**
  ```cmd
  myanswers 4
  ```
* **Experiment 5:**
  ```cmd
  myanswers 5
  ```

#### Option B: Interactive Menu
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
* Type `1` to `5` to view any experiment.
* Type `0` to exit.

---

## Method 2: Ultra-Fast 1-Line Direct View (No Scripts Needed at All)

If you are on a lab PC and just want the answer text immediately on your screen without downloading anything:

* **In PowerShell (Use `irm`):**
  ```powershell
  irm https://raw.githubusercontent.com/sujanshetty707/cisco/main/experiments/exp1.txt
  irm https://raw.githubusercontent.com/sujanshetty707/cisco/main/experiments/exp2.txt
  irm https://raw.githubusercontent.com/sujanshetty707/cisco/main/experiments/exp3.txt
  irm https://raw.githubusercontent.com/sujanshetty707/cisco/main/experiments/exp4.txt
  irm https://raw.githubusercontent.com/sujanshetty707/cisco/main/experiments/exp5.txt
  ```

* **In Command Prompt (CMD):**
  ```cmd
  curl https://raw.githubusercontent.com/sujanshetty707/cisco/main/experiments/exp3.txt
  ```

---

## Updating Answers (Optional)
If you ever want to update an experiment and push changes back to GitHub:
```cmd
myanswers update 3
```
*(Only this update/push action requires GitHub authentication with write permission).*

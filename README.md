# Lab Answers - Data Communication and Computer Network (CSE2252)

Private repository storing lab experiment answers, configuration steps, and CLI access tooling for Data Communication and Computer Network Lab (CSE2252).

> **CONFIDENTIALITY NOTICE**  
> This repository contains private study materials. Keep this repository **PRIVATE**. Never commit Personal Access Tokens, API keys, passwords, or personal credentials.

---

## Repository Structure

```text
lab-answers/
├── experiments/
│   ├── exp1.txt   # Basic Network Commands and Network Devices
│   ├── exp2.txt   # Basic Configuration of Switch/Router Using Cisco Packet Tracer
│   ├── exp3.txt   # Configure Privilege Level Password and User Authentication in Switch
│   ├── exp4.txt   # Configure DHCP Server and Wireless Router and Check Connectivity
│   └── exp5.txt   # Configure Static Routing Using Cisco Packet Tracer
├── myanswers.py   # Standalone Python CLI client (zero external dependencies)
├── myanswers.bat  # Windows launcher command
├── myanswers      # Linux/macOS launcher command
├── setup.py       # Optional package installer (pip install .)
├── .gitignore     # Git ignore rules for credentials, caches, and temp files
└── README.md      # Repository documentation and setup guide
```

---

## Experiments Overview

| No. | Experiment Title | Description |
|:---:|:---|:---|
| **1** | **Basic Network Commands and Network Devices** | Study of ping, ipconfig, tracert, nslookup, netstat, arp, getmac, route, and network hardware devices. |
| **2** | **Basic Configuration of Switch/Router Using Cisco Packet Tracer** | Router interface setup, switch initialization, clock, hostname, banner, and connectivity verification. |
| **3** | **Configure Privilege Level Password and User Authentication in Switch** | Console security, privilege level passwords (secret & plaintext), and local user authentication. |
| **4** | **Configure DHCP Server and Wireless Router and Check Connectivity** | DHCP IP distribution, wireless SSID and security configuration, wireless laptop/PC connectivity. |
| **5** | **Configure Static Routing Using Cisco Packet Tracer** | Static route configuration on multiple routers, next-hop forwarding, and end-to-end ping testing. |

---

## Quick Usage

### 1. Interactive Menu
```bash
myanswers
```

### 2. View Specific Experiment Directly
```bash
myanswers 3
```

### 3. Update an Experiment and Push to GitHub
```bash
myanswers update 3
```
Or update from a local file:
```bash
myanswers update 3 new_exp3.txt
```

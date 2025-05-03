
# 🛡️ GhostOps Red Team Lab: `loot_drop.py` Encrypted Exfiltration

Welcome to the GhostOps portfolio lab — a hands-on red team operation that simulates encrypted data exfiltration using custom AES encryption and HTTPS delivery via Flask. This lab demonstrates post-exploitation tactics ideal for adversary emulation and threat simulation.

---

## 🚀 Project Summary

- **Reverse Shell Used:** HTTPS + AES encrypted shell
- **Exfiltration Method:** Python-based AES-CBC + HTTPS POST
- **Target:** Kali Linux VM
- **Listener:** Hardened Windows system with Flask HTTPS server

---

## 📁 Project Structure

```
redteam/
├── cert.pem              # TLS certificate (self-signed)
├── key.pem               # TLS private key
├── listener_https.py     # HTTPS Flask listener (receives loot)
├── loot_drop.py          # Payload executed on compromised target
└── README.md             # 🔥 You are here!
```

---

## 🔒 Features

- AES-256 CBC file encryption
- IV generation and Base64 transfer
- HTTPS endpoint with Flask
- Traffic blending with normal POSTs
- Hardened listener environment
- Minimal dependencies

---

## 🔧 Dependencies

On **target (Kali)**:

```bash
pip3 install requests pycryptodome
```

---

## 📡 Listener Setup (Host)

```bash
# Activate virtual environment
Set-ExecutionPolicy -Scope Process Bypass
& "C:\Users\user\Dev\pyenv31013\Scripts\Activate.ps1"

# Launch Flask server
& "C:\Users\user\Dev\PCbuild\amd64\python.exe" listener_https.py
```

Server will run on:
```
https://127.0.0.1:443
https://10.0.0.201:443
```

---

## 🎯 Target Execution (Kali)

```bash
python3 loot_drop.py
```

> Status: 200 means the payload was delivered and captured.

---

## 🔍 What We Accomplished

- Created a **secure exfiltration channel** with encryption + HTTPS
- Deployed and executed **payloads post-compromise**
- Emulated real-world **red team file theft over TLS**
- Bypassed hardened host restrictions using a custom Python build

---

## 🛠️ Future Improvements

- Add automatic zip and drop directory
- Covert exfil (DNS / ICMP tunnel)
- Xor + AES hybrid obfuscation
- File watcher + timed drops

---

## 📸 Screenshots

> Be sure to include:
> - Flask listener output
> - Encrypted AES payload
> - Kali loot execution
> - Wireshark traffic trace

---

> 🧠 **Built for adversary simulation. Studied for defense. Inspired by Ghost in the Shell.**

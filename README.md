# 🕵️‍♂️ GhostOps — Cybersecurity Recon, Exploitation & Detection Toolkit

A monorepo containing four powerful offensive and defensive cybersecurity tools, developed to simulate real‑world adversary operations, defend networks, and perform intelligent reconnaissance at scale.

---

## 🧩 Projects Overview

| Icon | Project                     | Description                                                                 |
|:----:|-----------------------------|-----------------------------------------------------------------------------|
| 🧠   | **GhostOps Recon**          | Automated OSINT & Attack Surface Mapping (CLI + CVE Intelligence)           |
| 🔥   | **GhostOps Red Team Lab**   | Encrypted Reverse Shell & AES Data Exfiltration                             |
| 👁️   | **SpecterOps Sentinel**     | ML‑Based Network Anomaly Detection with Live Packet Scoring                 |
| 🛡️   | **GhostOps HoneyGuard**     | Low‑Interaction, ML‑Enhanced Honeypot for Attacker Behavior Logging & Alerting |

---

## 🚀 GhostOps Recon

**Purpose:** Pre‑exploitation intelligence and vulnerability detection

**What It Does:**
- WHOIS & DNS reconnaissance  
- Subdomain brute‑forcing  
- Asynchronous TCP port scanning with banner grabbing  
- Tech fingerprinting via HTTP headers & favicon hashes  
- Real‑time CVE matching using the NVD API  
- Integration with Sentinel for CVE‑tagged anomalies  
- Streamlit dashboard for visual analysis  

**Workflow:**
Targets → Recon Orchestrator →
├─ Domain Mapping (WHOIS/DNS/Subdomains)
├─ Port Scanning (async)
├─ Tech Profiler (Headers + Favicon)
├─ CVE Correlation (NVD API)
└─ JSON Reports + Streamlit Dashboard

📁 See [`ghostops_recon/README.md`](ghostops_recon/README.md)

---

## 🔥 GhostOps Red Team Lab

**Purpose:** Simulate post‑exploitation behavior with encrypted exfiltration

**What It Does:**
- AES‑256 CBC encrypted data exfiltration via HTTPS POST  
- Reverse‑shell payload delivered to a hardened Flask listener  
- Self‑signed certificate TLS support  
- Designed to emulate real‑world adversary tradecraft  

**Workflow:**
Target (Kali) →
loot_drop.py (AES‑CBC Encrypt & Exfil via POST) →
listener_https.py (Flask listener on Windows Hardened VM) →
Decrypt & Store Exfiltrated Data

📁 See [`redteam/README.md`](redteam/README.md)

---

## 👁️ SpecterOps Sentinel

**Purpose:** Defend networks with intelligent ML‑based packet anomaly detection

**What It Does:**
- Trains an Isolation Forest on PCAPs  
- Scores live or replayed network streams for anomalies  
- Feature pipeline: entropy, TTL, ports, TCP flags, IAT, direction  
- Flags suspicious flows and optionally enriches with Recon CVEs  

**Workflow:**
PCAP or Live Interface →
Feature Extraction →
Train Model →
Evaluate (ROC/AUC + cutoff tuning) →
Live Detection (sniffer or replay) →
Output anomalies → Optional CVE enrichment

📁 See [`SpecterOps_Sentinel/README.md`](SpecterOps_Sentinel/README.md)

---

## 🛡️ GhostOps HoneyGuard

**Purpose:** Actively lure attackers, log their behavior, and classify anomalous sessions

**What It Does:**
- **Service Emulation:** Fake SSH (22), HTTP (80/443), and MySQL (3306) listeners  
- **Structured Logging:** Records connection start/end, banners, inputs, HTTP requests, MySQL auth packets in `logs/events.jsonl`  
- **Feature Extraction:** Converts event logs to session metrics (`features.py`)  
- **Anomaly Detection:** Trains an Isolation Forest on those features (`classifier.py`)  
- **Session Classification:** Outputs `predictions.csv` with `anomaly_score` & `label`  
- **Dashboard Integration:** View alerts alongside Recon & Sentinel in Streamlit  

**Workflow:**
Attacker → HoneyGuard Server →
├─ Emulated Service Handlers (SSH, HTTP, MySQL)
├─ Async Logging (logger.py → events.jsonl)
├─ Feature Engineering (features.py → features.csv)
├─ Model Training (classifier.py train → models/)
└─ Prediction (classifier.py predict → predictions.csv)

📁 See [`honeyguard/README.md`](honeyguard/README.md)

---

## 🧰 Install & Use

Each sub‑project is self‑contained and installable:

```bash
# GhostOps Recon
cd ghostops_recon && pip install . 
ghostrecon scan example.com

# GhostOps Red Team Lab
cd redteam && pip install -r requirements.txt 
python listener_https.py

# SpecterOps Sentinel
cd SpecterOps_Sentinel && pip install -r requirements.txt 
python train_model.py

# GhostOps HoneyGuard
cd honeyguard && pip install -r requirements.txt
python -m honeyguard.server
Launch the unified Streamlit dashboard:

cd dashboard
streamlit run web_ui.py
🧠 Why This Matters
Together, these tools simulate the full red‑blue spectrum of cybersecurity operations:

🔎 Identify attack surface (GhostOps Recon)

🎯 Emulate adversary tradecraft (Red Team Lab & HoneyGuard)

🚨 Detect and investigate anomalies (SpecterOps Sentinel)

Ideal for:

Offensive security professionals

Threat hunters

ML researchers in cybersecurity

Advanced red team training

📜 License
This repo is licensed under the MIT License. See LICENSE for details.

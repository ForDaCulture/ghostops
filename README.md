# 🕵️‍♂️ GhostOps — Cybersecurity Recon, Exploitation & Detection Toolkit

A monorepo containing three powerful offensive and defensive cybersecurity tools, developed to simulate real-world adversary operations, defend networks, and perform intelligent recon at scale.

---

## 🧩 Projects Overview

| Project                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| 🧠 **GhostOps Recon**        | Automated OSINT + Attack Surface Mapping (CLI + CVE Intelligence)         |
| 🔥 **GhostOps Red Team Lab** | Encrypted Reverse Shell & AES Data Exfiltration                          |
| 👁️ **SpecterOps Sentinel**   | Machine Learning-Based Network Anomaly Detection with Live Packet Scoring |

---

## 🚀 GhostOps Recon

**Purpose:** Pre-exploitation intelligence and vulnerability detection

**What It Does:**
- WHOIS & DNS recon
- Subdomain brute-forcing
- Async TCP port scanning with banner grabbing
- Tech fingerprinting from HTTP headers and favicon hashes
- Real-time CVE matching using the NVD API
- Integration with Sentinel for CVE-tagged anomalies
- Streamlit dashboard for visual analysis

**Workflow:**

```text
Targets → Recon Orchestrator →
    ├─ Domain Mapping (WHOIS/DNS/Subdomains)
    ├─ Port Scanning (async)
    ├─ Tech Profiler (Headers + Favicon)
    ├─ CVE Correlation (NVD API)
    └─ JSON Reports + Streamlit Dashboard
📁 See ghostops_recon/README.md

🔥 GhostOps Red Team Lab
Purpose: Simulate post-exploitation behavior with encrypted exfiltration

What It Does:

AES-256 CBC encrypted data exfiltration via HTTPS POST

Reverse shell payload delivered to hardened Flask listener

Self-signed cert TLS support

Built for emulating real-world threat actor tradecraft

Workflow:

text
Copy
Edit
Target (Kali) →
    loot_drop.py (AES-CBC Encrypt & Exfil via POST) →
        listener_https.py (Flask listener on Windows Hardened VM) →
            Decrypt & Store Exfiltrated Data
📁 See redteam/README.md

👁️ SpecterOps Sentinel
Purpose: Defend networks with intelligent ML-based packet anomaly detection

What It Does:

Trains Isolation Forest model on PCAPs

Scores live/replayed packet streams for anomalies

Feature-rich pipeline:

Entropy, TTL, ports, TCP flags, IAT, direction

Flags suspicious flows, integrates with GhostOps Recon CVEs

Workflow:
PCAP or Live Interface →
    Feature Extraction →
        Train Model →
            Evaluate (ROC/AUC + cutoff tuning) →
                Live Detection (sniffer or replay) →
                    Output anomalies → Optional CVE enrichment
📁 See SpecterOps_Sentinel/README.md

🧰 Install & Use
Each project is self-contained and installable:

bash
Copy
Edit
cd ghostops_recon && pip install .
ghostrecon scan example.com
Or explore ML-based detection and encrypted post-exploitation in SpecterOps_Sentinel/ and redteam/.

🧠 Why This Matters
Together, these projects simulate the full red-blue spectrum of cybersecurity operations:

🔎 Identify attack surface (GhostOps Recon)

🚨 Trigger and investigate anomalies (SpecterOps Sentinel)

🎯 Emulate adversary behavior post-breach (GhostOps Red Team Lab)

They are ideal for:

Offensive security professionals

Threat hunters

ML researchers in cybersecurity

Advanced red team training

📜 License
This repo is licensed under the MIT License. See LICENSE.

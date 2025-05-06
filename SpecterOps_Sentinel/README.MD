# SpecterOps Sentinel

**SpecterOps Sentinel** is a modular, feature‑engineered machine‑learning pipeline for detecting network anomalies in packet captures. Built as part of the **GhostOps** portfolio, this project demonstrates end‑to‑end cybersecurity and ML expertise.

---

## 🚀 Key Features

- **Rich Feature Set**  
  - Packet length, IP protocol, TTL  
  - Payload entropy & entropy/length ratio  
  - Inter‑arrival time (IAT)  
  - Source/destination ports, TCP flags, SYN‑without‑ACK  
  - Traffic direction (inbound vs outbound), port common vs ephemeral ratio

- **Four‑Stage Pipeline**  
  1. **Training** (`train_model.py`): Builds an IsolationForest on benign traffic.  
  2. **Evaluation** (`evaluate_model.py`): Computes ROC/AUC; finds optimal threshold.  
  3. **Offline Analysis** (`analyze_pcap.py`): Scores PCAPs, flags anomalies with a fixed cutoff.  
  4. **Live Sniffer** (`tools/anomaly_sniffer.py`): Real‑time anomaly detection on interfaces or replay.

- **Data‑Driven Tuning**  
  - Adjustable contamination for training  
  - ROC‑based or fixed‑offset cutoff selection  
  - Placeholder‑driven CLI for your network (`<PCAP_PATH>`, `<LOCAL_IP>`, `<INTERFACE>`)

---

## 📁 Repository Structure
SpecterOps_Sentinel/
├── data/ # (not tracked) your PCAPs & model outputs
├── tools/
│ ├── anomaly_sniffer.py # Live/offline sniffer
│ └── dns_exfil_classifier.py
├── train_model.py
├── evaluate_model.py
├── analyze_pcap.py
├── requirements.txt
├── tests/
│ └── test_dns_exfil.py
└── README.md


---

## 🔧 Installation

```bash
git clone https://github.com/<YOUR_USERNAME>/GhostOps.git
cd GhostOps/SpecterOps_Sentinel

python3 -m venv venv
source venv/bin/activate        # macOS/Linux
.\venv\Scripts\Activate.ps1     # Windows PowerShell

pip install -r requirements.txt

🎓 How to Use
1. Train the Model
bash
python train_model.py \
  --pcap data/benign.pcap \
  --model data/model.joblib \
  --local-ip <YOUR_HOST_IP> \
  --contamination 0.001
2. Evaluate Performance
bash
Copy
Edit
python evaluate_model.py \
  --benign data/benign.pcap \
  --malicious data/malicious.pcap \
  --model data/model.joblib \
  --local-ip <YOUR_HOST_IP>
3. Offline PCAP Analysis
bash
Copy
Edit
python analyze_pcap.py \
  --pcap data/target.pcap \
  --model data/model.joblib \
  --local-ip <YOUR_HOST_IP> \
  --cutoff <THRESHOLD>
4. Live Anomaly Sniffer
bash
Copy
Edit
python tools/anomaly_sniffer.py \
  --iface <INTERFACE> \
  --model data/model.joblib \
  --local-ip <YOUR_HOST_IP> \
  --threshold 0.05
📈 Fine‑Tuning Workflow
Pick a contamination rate for expected anomalies (e.g. 0.001).

Train on benign traffic.

Evaluate via ROC to find AUC & optimal cutoff.

Analyze benign & malicious PCAPs to confirm FP/TP rates.

Adjust contamination or cutoff until you hit your target (e.g. < 1 % FP, > 70 % TP).

📜 License
This project is licensed under the MIT License.
Feel free to fork and adapt for your own security automations!


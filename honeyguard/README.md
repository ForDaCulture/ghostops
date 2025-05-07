# 🛡️ GhostOps HoneyGuard

**GhostOps HoneyGuard** is a low‑interaction, ML‑enhanced honeypot designed to lure adversaries, capture their tactics, and intelligently classify attacker behavior. As a portfolio centerpiece, HoneyGuard showcases full‑stack cybersecurity skills—from asynchronous network programming through data engineering to machine learning and dashboard visualization.

---

## 🌟 Highlights

- **Multi‑Protocol Emulation**  
  - **SSH** on port 22 with realistic banner and authentication stub  
  - **HTTP/HTTPS** on ports 80 & 443 with 404 responses and request capture  
  - **MySQL** on port 3306 with dummy handshake and auth‑packet logging  

- **Structured, JSON‑Lines Logging**  
  - All events (`connection_start`, banners, inputs, HTTP requests, auth packets, `connection_end`) are recorded to `logs/events.jsonl`  
  - Designed for easy ingestion into Elastic, Splunk, or custom feature pipelines  

- **Automated Feature Engineering**  
  - `features.py` parses logs into per‑session metrics (event counts, byte volumes, request types)  
  - Outputs `features.csv` ready for machine learning  

- **Anomaly Detection with IsolationForest**  
  - `classifier.py` trains on session features to learn “normal” vs. “anomalous”  
  - Generates `predictions.csv` with `anomaly_score` and `label` for each session  

- **Streamlit Dashboard Integration**  
  - View and download anomalies alongside forensic recon data  
  - Highlights suspicious sessions in‑line for rapid triage  

---

## 🛠️ Installation

1. **Clone & Navigate**  
   ```bash
   git clone https://github.com/ForDaCulture/ghostops.git
   cd ghostops/honeyguard
Create & Activate Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate         # macOS/Linux
venv\Scripts\Activate.ps1        # Windows PowerShell
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
(Optional) Configure Logging Path
By default, logs go to logs/events.jsonl. To change, set environment variable:

bash
Copy
Edit
export HONEYGUARD_LOG_DIR="/path/to/logs"
🚀 Usage
1. Start the Honeypot
bash
Copy
Edit
python -m honeyguard.server
HoneyGuard will silently listen on ports 22, 80, 443, and 3306.

2. Generate Attack Events
In a new terminal, trigger activity:

bash
Copy
Edit
curl http://localhost:80/test
ssh -p 22 attacker@localhost
mysql -h 127.0.0.1 -P 3306 -u root -proot
3. Extract Features
bash
Copy
Edit
python -m honeyguard.features
# → Creates features.csv
4. Train Anomaly Model
bash
Copy
Edit
python -m honeyguard.classifier train \
    --features features.csv \
    --contamination 0.05
# → Saves models/honeyguard_iforest.joblib
5. Predict & Label Sessions
bash
Copy
Edit
python -m honeyguard.classifier predict \
    --features features.csv \
    --output predictions.csv
6. Visualize in Dashboard
Upload predictions.csv to your Streamlit dashboard alongside Recon data:

bash
Copy
Edit
cd ../dashboard
streamlit run web_ui.py
📂 Architecture
graphql
Copy
Edit
honeyguard/
├── __init__.py
├── server.py         # Asyncio server & dispatcher
├── logger.py         # JSON‑lines event logger (non‑blocking)
├── handlers/         # Fake protocol implementations
│   ├── __init__.py
│   ├── ssh.py        # SSH banner & input capture
│   ├── http.py       # HTTP request capture & 404 response
│   └── mysql.py      # MySQL handshake & auth capture
├── features.py       # Parses logs → session metrics
├── classifier.py     # Trains/predicts with IsolationForest
└── requirements.txt
logs/                  # JSON‑lines attack event logs
models/                # Serialized ML models (.joblib)
🎯 Why HoneyGuard?
Demonstrates End‑to‑End Skills: network programming, asynchronous I/O, logging design, data processing, machine learning, and web visualization.

Real‑World Relevance: mimics common attack surfaces and integrates with threat‑intelligence workflows.

Portfolio‑Ready: a standout project showing how to build a full attack‑defense lifecycle tool from scratch.

🚧 Future Enhancements
Additional Protocols: SMTP, FTP, Redis, etc.

Real‑Time Alerting: Slack/Webhook integration for high‑severity sessions.

Advanced ML: Deep learning sequence models for richer behavior analysis.

Containerization: Docker image for easy deployment.

📜 License
This project is licensed under the MIT License. See LICENSE for details.

Built by ForDaCulture — exploring the frontier where offensive tooling meets intelligent defense.

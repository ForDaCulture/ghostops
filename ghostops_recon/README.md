# 🧠 GhostOps Recon

**GhostOps Recon** is a modular, installable Python CLI tool for automated OSINT and attack surface mapping. Designed for Red Teams, SOCs, and cybersecurity analysts.

## 🚀 Features

- WHOIS & DNS Reconnaissance
- Subdomain brute-force
- Async TCP Port Scanning + Banner Grabbing
- Web Tech Stack Fingerprinting (Headers + Favicon Hash)
- Live CVE Lookup via NVD API
- Batch Mode for Mass Recon
- Streamlit Dashboard (optional)
- SpecterOps Sentinel CVE Alert Hook

## 🧱 Install

```bash
git clone https://github.com/YOUR_GITHUB/ghostops_recon.git
cd ghostops_recon
pip install .
```

## 📟 Usage

```bash
ghostrecon scan example.com
ghostrecon batch targets.txt
```

Outputs saved to: `batch_reports/report_<target>.json`

## 📊 Dashboard

```bash
streamlit run dashboard/web_ui.py
```

## ⚠️ CVE Lookup

Create `.env` from the example:

```
NVD_API_KEY=your-api-key-here
```

Register for a free key: https://nvd.nist.gov/developers/request-an-api-key

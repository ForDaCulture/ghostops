#!/usr/bin/env python3
"""
Live or offline packet anomaly sniffer. Logs anomalies to rotating file.
Usage:
  python tools/anomaly_sniffer.py \
    --iface <INTERFACE|.pcap> \
    --model <MODEL_PATH>/model.joblib \
    --local-ip <LOCAL_IP> \
    --threshold 0.05
"""
import os
import argparse
import logging
import joblib
import numpy as np
from logging.handlers import RotatingFileHandler
from scapy.all import sniff, IP, TCP

from train_model import extract_features

# Logging setup
logger = logging.getLogger("anomaly_sniffer")
if not logger.handlers:
    h = RotatingFileHandler("anomaly_sniffer.log", maxBytes=5e6, backupCount=3)
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(h)

def main(iface, model_path, local_ip, threshold):
    model = joblib.load(model_path)
    logger.info(f"Model loaded; threshold={threshold}")

    def handle(pkt):
        try:
            feats = extract_features(pkt, local_ip)
            vec   = np.array([feats[k] for k in [
                "length","protocol","entropy","iat",
                "src_port","dst_port","ttl","flags",
                "direction","syn_no_ack","port_common_ratio","entropy_len_ratio"
            ]]).reshape(1, -1)
            score = model.decision_function(vec)[0]
            if score < -threshold:
                logger.warning(f"ANOMALY score={score:.3f}")
        except Exception as e:
            logger.error(f"Error: {e}")

    offline = os.path.isfile(iface) and iface.lower().endswith(".pcap")
    mode    = "PCAP replay" if offline else f"live iface {iface}"
    logger.info(f"Starting {mode}")

    sniff(iface=None if offline else iface,
          offline=iface if offline else None,
          prn=handle, store=False)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--iface",     required=True)
    p.add_argument("--model",     required=True)
    p.add_argument("--local-ip",  required=True)
    p.add_argument("--threshold", type=float, default=0.05)
    args = p.parse_args()
    main(args.iface, args.model, args.local_ip, args.threshold)

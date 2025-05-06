#!/usr/bin/env python3
"""
Evaluate the trained model using ROC/AUC on benign vs malicious PCAPs.
Usage:
  python evaluate_model.py \
    --benign <PCAP_PATH>/benign.pcap \
    --malicious <PCAP_PATH>/malicious.pcap \
    --model <MODEL_PATH>/model.joblib \
    --local-ip <LOCAL_IP>
"""
import argparse
import numpy as np
import joblib
from sklearn.metrics import roc_curve, auc
from scapy.all import rdpcap, IP, TCP, UDP
from train_model import extract_features

def get_scores(pcap_path, model, local_ip):
    pkts = rdpcap(pcap_path)
    scores = []
    for pkt in pkts:
        feats = extract_features(pkt, local_ip)
        vec = np.array([feats[k] for k in [
            "length","protocol","entropy","iat",
            "src_port","dst_port","ttl","flags",
            "direction","syn_no_ack","port_common_ratio","entropy_len_ratio"
        ]]).reshape(1, -1)
        scores.append(model.decision_function(vec)[0])
    return np.array(scores)

def main(benign_pcap, malicious_pcap, model_path, local_ip):
    model    = joblib.load(model_path)
    scores_b = get_scores(benign_pcap,   model, local_ip)
    scores_m = get_scores(malicious_pcap, model, local_ip)

    y_true  = np.concatenate([np.zeros_like(scores_b), np.ones_like(scores_m)])
    y_score = np.concatenate([-scores_b, -scores_m])  # flip so higher = malicious

    fpr, tpr, thr = roc_curve(y_true, y_score)
    roc_auc      = auc(fpr, tpr)
    j_scores     = tpr - fpr
    ix           = np.argmax(j_scores)

    print(f"AUC = {roc_auc:.3f}")
    print(f"Optimal threshold = {thr[ix]:.3f} → FPR {fpr[ix]:.3%}, TPR {tpr[ix]:.3%}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--benign",    default="data/benign.pcap")
    p.add_argument("--malicious", default="data/malicious.pcap")
    p.add_argument("--model",     default="data/model.joblib")
    p.add_argument("--local-ip",  required=True)
    args = p.parse_args()
    main(args.benign, args.malicious, args.model, args.local_ip)

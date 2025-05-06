#!/usr/bin/env python3
"""
Train an IsolationForest on benign PCAP traffic, using a rich set of packet features.
Usage:
  python train_model.py \
    --pcap <PCAP_PATH>/benign.pcap \
    --model <MODEL_PATH>/model.joblib \
    --local-ip <LOCAL_IP> \
    --contamination 0.001
"""
import argparse
import pandas as pd
import numpy as np
from scapy.all import rdpcap, IP, TCP, UDP
from sklearn.ensemble import IsolationForest
import joblib

last_ts = None

def compute_payload_entropy(payload: bytes) -> float:
    if not payload:
        return 0.0
    freq = np.bincount(np.frombuffer(payload, dtype=np.uint8), minlength=256)
    prob = freq / freq.sum()
    prob = prob[prob > 0]
    entropy = -np.sum(prob * np.log2(prob))
    return entropy / 8.0

def extract_features(pkt, local_ip):
    global last_ts
    ts = float(pkt.time)
    iat = 0.0 if last_ts is None else ts - last_ts
    last_ts = ts

    raw = bytes(pkt)
    length = len(raw)

    if IP in pkt:
        ip       = pkt[IP]
        protocol = ip.proto
        ttl      = ip.ttl
        l4       = ip.payload
        src_ip   = ip.src
    else:
        protocol = ttl = 0
        l4 = None
        src_ip = None

    src_port = getattr(l4, 'sport', 0)
    dst_port = getattr(l4, 'dport', 0)
    flags    = int(l4.flags) if isinstance(l4, TCP) else 0

    payload = bytes(getattr(l4, 'payload', b""))
    entropy = compute_payload_entropy(payload)

    direction         = 1 if src_ip == local_ip else 0
    syn_no_ack        = 1 if isinstance(l4, TCP) and (flags & 0x02) and not (flags & 0x10) else 0
    port_common_ratio = ((src_port < 1024) + (dst_port < 1024)) / 2.0
    ent_len_ratio     = entropy / length if length > 0 else 0.0

    return {
        "length":            length,
        "protocol":          protocol,
        "entropy":           entropy,
        "iat":               iat,
        "src_port":          src_port,
        "dst_port":          dst_port,
        "ttl":               ttl,
        "flags":             flags,
        "direction":         direction,
        "syn_no_ack":        syn_no_ack,
        "port_common_ratio": port_common_ratio,
        "entropy_len_ratio": ent_len_ratio,
    }

def train(pcap_path, model_path, local_ip, contamination):
    print(f"Loading PCAP: {pcap_path}")
    pkts = rdpcap(pcap_path)

    feats = [extract_features(pkt, local_ip) for pkt in pkts]
    df = pd.DataFrame(feats)
    print("Sample features:\n", df.head(), "\n")

    X = df[[
        "length","protocol","entropy","iat",
        "src_port","dst_port","ttl","flags",
        "direction","syn_no_ack","port_common_ratio","entropy_len_ratio"
    ]].values

    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)
    joblib.dump(model, model_path)
    print(f"\n✅ Model saved to {model_path} (contamination={contamination})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pcap",          default="data/benign.pcap")
    parser.add_argument("--model",         default="data/model.joblib")
    parser.add_argument("--local-ip",      required=True)
    parser.add_argument("--contamination", type=float, default=0.001)
    args = parser.parse_args()
    train(args.pcap, args.model, args.local_ip, args.contamination)

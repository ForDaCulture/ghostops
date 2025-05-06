#!/usr/bin/env python3
"""
Analyze a PCAP offline, flagging packets whose anomaly score falls below the cutoff.
Usage:
  python analyze_pcap.py \
    --pcap <PCAP_PATH>/target.pcap \
    --model <MODEL_PATH>/model.joblib \
    --local-ip <LOCAL_IP> \
    [--cutoff <THRESHOLD>]
"""
import argparse
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from scapy.all import rdpcap, IP, TCP
from train_model import extract_features

def main(pcap_path, model_path, local_ip, cutoff):
    model = joblib.load(model_path)

    if cutoff is None:
        cutoff = model.offset_
        print(f"Using model.offset_ cutoff = {cutoff:.3f}")
    else:
        print(f"Using custom cutoff = {cutoff:.3f}")

    print(f"Reading PCAP: {pcap_path}")
    pkts = rdpcap(pcap_path)

    rows, scores = [], []
    for pkt in pkts:
        ts = float(pkt.time)
        timestamp = pd.to_datetime(ts, unit="s")

        feats = extract_features(pkt, local_ip)
        vec   = np.array([feats[k] for k in [
            "length","protocol","entropy","iat",
            "src_port","dst_port","ttl","flags",
            "direction","syn_no_ack","port_common_ratio","entropy_len_ratio"
        ]]).reshape(1, -1)
        score = model.decision_function(vec)[0]

        feats.update({
            "timestamp": timestamp,
            "score":     score
        })
        rows.append(feats)
        scores.append(score)

    df = pd.DataFrame(rows).set_index("timestamp")
    scores = pd.Series(scores, index=df.index)

    print("\nScore Statistics:")
    print(f"  min:    {scores.min():.3f}")
    print(f"  25th%:  {scores.quantile(0.25):.3f}")
    print(f"  median: {scores.median():.3f}")
    print(f"  75th%:  {scores.quantile(0.75):.3f}")
    print(f"  max:    {scores.max():.3f}")

    df["flagged"] = scores < cutoff
    total   = len(df)
    flagged = df["flagged"].sum()
    print(f"\nCutoff: {cutoff:.3f}")
    print(f"Flagged: {flagged}/{total} ({flagged/total:.2%})")
    print("By protocol:")
    print(df[df.flagged].groupby("protocol").size(), "\n")

    df.to_csv("data/pcap_analysis.csv")
    print("Saved analysis to data/pcap_analysis.csv")

    plt.figure(figsize=(8,4))
    scores.hist(bins=50)
    plt.axvline(cutoff, color="red", linestyle="--", label=f"cutoff {cutoff:.3f}")
    plt.title("Anomaly Score Distribution")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pcap",     default="data/benign.pcap")
    p.add_argument("--model",    default="data/model.joblib")
    p.add_argument("--local-ip", required=True)
    p.add_argument("--cutoff",   type=float, default=None)
    args = p.parse_args()
    main(args.pcap, args.model, args.local_ip, args.cutoff)

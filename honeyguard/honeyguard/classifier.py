# classifier.py
# Train and run an IsolationForest model on your honeypot session features.

import os
import argparse
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# 1. Paths & Constants
MODEL_DIR = os.getenv("HONEYGUARD_MODEL_DIR", "models")
MODEL_FILE = os.path.join(MODEL_DIR, "honeyguard_iforest.joblib")
DEFAULT_FEATURES = "features.csv"  # output from features.py

def train_model(features_csv: str, contamination: float = 0.05):
    """
    2. Train an IsolationForest on the feature CSV.
       - contamination: expected fraction of anomalies.
       - saves a joblib model in MODEL_DIR.
    """
    # Ensure model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Load the features
    df = pd.read_csv(features_csv)
    # Drop non‑numeric or identifier columns
    X = df.drop(columns=["src_ip", "port"])

    # Initialize & train the model
    clf = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )
    clf.fit(X)

    # Persist the trained model
    joblib.dump(clf, MODEL_FILE)
    print(f"[✓] Model trained and saved to {MODEL_FILE}")

def predict_sessions(features_csv: str, output_csv: str = "predictions.csv"):
    """
    3. Load the trained model, score new feature sessions, and classify:
       - anomaly_score: lower means more anomalous
       - label: 1 for normal, -1 for anomaly
       - Saves predictions to output_csv.
    """
    # Load data & model
    df = pd.read_csv(features_csv)
    X = df.drop(columns=["src_ip", "port"])
    clf = joblib.load(MODEL_FILE)
    
    # Compute anomaly scores and labels
    scores = clf.decision_function(X)
    labels = clf.predict(X)

    # Attach back to DataFrame
    df["anomaly_score"] = scores
    df["label"] = labels

    # Save results
    df.to_csv(output_csv, index=False)
    print(f"[✓] Predictions written to {output_csv}")

def main():
    parser = argparse.ArgumentParser(prog="honeyguard_classifier",
                                     description="Train or predict with HoneyGuard IsolationForest")
    sub = parser.add_subparsers(dest="command", required=True)

    # Train subcommand
    t = sub.add_parser("train", help="Train anomaly detection model")
    t.add_argument("--features", default=DEFAULT_FEATURES,
                   help="Path to features CSV (src_ip,port,features...)")
    t.add_argument("--contamination", type=float, default=0.05,
                   help="Fraction of outliers expected (default 0.05)")

    # Predict subcommand
    p = sub.add_parser("predict", help="Classify sessions with trained model")
    p.add_argument("--features", default=DEFAULT_FEATURES,
                   help="Path to features CSV")
    p.add_argument("--output", default="predictions.csv",
                   help="Where to save labeled sessions")

    args = parser.parse_args()

    if args.command == "train":
        train_model(args.features, args.contamination)
    elif args.command == "predict":
        predict_sessions(args.features, args.output)

if __name__ == "__main__":
    main()

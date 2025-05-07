# features.py
# Load JSON‑lines events and extract per-session features for ML classification.

import json
from collections import defaultdict
import os

# Path to the JSON‑lines log
LOG_FILE = os.getenv("HONEYGUARD_LOG_DIR", "logs") + "/events.jsonl"

def load_events():
    """Read events.jsonl and return a list of dicts."""
    events = []
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            events.append(json.loads(line))
    return events

def extract_features(events):
    """
    Group events by (src_ip, port) session, then compute features:
      - total_events: total log entries in session
      - banner_events: count of 'ssh_banner_sent'
      - http_requests: count of 'http_request'
      - mysql_auths: count of 'mysql_auth_packet'
      - total_bytes: approximate sum of byte lengths of inputs (where present)
    Returns a dict mapping (src_ip, port) → feature dict.
    """
    sessions = defaultdict(list)
    for ev in events:
        key = (ev.get('src_ip'), ev.get('port'))
        sessions[key].append(ev)

    feature_set = {}
    for (src_ip, port), ev_list in sessions.items():
        total = len(ev_list)
        ssh_banners = sum(1 for e in ev_list if e['event']=='ssh_banner_sent')
        http_reqs   = sum(1 for e in ev_list if e['event']=='http_request')
        mysql_auths = sum(1 for e in ev_list if e['event']=='mysql_auth_packet')
        # Estimate bytes from length of 'input' or 'auth_hex'
        total_bytes = 0
        for e in ev_list:
            if 'input' in e:
                total_bytes += len(e['input'].encode('utf-8'))
            if 'auth_hex' in e:
                total_bytes += len(e['auth_hex']) // 2  # hex → bytes

        feature_set[(src_ip, port)] = {
            'total_events': total,
            'ssh_banners': ssh_banners,
            'http_requests': http_reqs,
            'mysql_auths': mysql_auths,
            'total_bytes': total_bytes
        }
    return feature_set

def save_features(features, output_path="features.csv"):
    """
    Save the feature dict to a CSV file for further ML processing.
    """
    import csv
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['src_ip','port','total_events','ssh_banners','http_requests','mysql_auths','total_bytes'])
        # Rows
        for (src_ip, port), feat in features.items():
            writer.writerow([
                src_ip, port,
                feat['total_events'],
                feat['ssh_banners'],
                feat['http_requests'],
                feat['mysql_auths'],
                feat['total_bytes']
            ])
    print(f"[✓] Features written to {output_path}")

if __name__ == "__main__":
    evs = load_events()
    feats = extract_features(evs)
    save_features(feats)

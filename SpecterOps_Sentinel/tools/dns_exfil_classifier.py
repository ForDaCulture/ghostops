"""
Stub classifier for DNS exfil detection. Example of additional CyberAI Pack tool.
"""
def classify_query(q: str) -> str:
    # Replace with actual entropy‐based logic
    return "anomalous" if len(q) < 20 else "normal"

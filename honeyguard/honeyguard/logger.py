# ghostops_honeyguard/logger.py
# Asynchronous JSON‑line event logger for HoneyGuard honeypot.

import asyncio
import json
import os
from datetime import datetime

# 1. Path to the log file (adjustable)
LOG_DIR = os.getenv("HONEYGUARD_LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "events.jsonl")

def _ensure_log_dir():
    """Synchronously create the log directory if it doesn't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)

def _write_event(line: str):
    """
    Synchronously write a single JSON line to the log file.
    Appends with newline for JSON‑lines format.
    """
    _ensure_log_dir()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

async def log_event(event: dict):
    """
    Asynchronously log an event dict to the JSON‑lines file.
    
    Steps:
      1. Add a human-readable UTC timestamp.
      2. Serialize the event to JSON.
      3. Use run_in_executor to call the blocking file write off the event loop.
    """
    # 2. Enrich event with ISO‑8601 timestamp
    event["timestamp_utc"] = datetime.utcnow().isoformat() + "Z"
    
    # 3. Serialize to JSON string
    line = json.dumps(event, ensure_ascii=False)
    
    # 4. Offload file I/O to default ThreadPoolExecutor
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _write_event, line)

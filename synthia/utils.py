from datetime import datetime
import os

LOG_PATH = "data/log.txt"

def log(msg, level="info"):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] [{level.upper()}] {msg}"
    print(entry)
    os.makedirs("data", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")

import json

def load_config():
    try:
        with open("/data/options.json", "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"Failed to load config: {e}", "error")
        return {}

state = {
    "log_level": "debug",
    "enable_notifications": False
}

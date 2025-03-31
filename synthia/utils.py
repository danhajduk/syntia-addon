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

from datetime import datetime

LOG_PATH = "data/log.txt"

def log(msg, level="info"):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] [{level.upper()}] {msg}"
    print(entry)
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")

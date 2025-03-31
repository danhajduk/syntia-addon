import json
import time
from datetime import datetime
import os

LOG_PATH = "data/log.txt"

def log(message, level="info"):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] [{level.upper()}] {message}"
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")
    print(entry)

def load_config():
    try:
        with open("/data/options.json") as f:
            return json.load(f)
    except Exception as e:
        log(f"Error loading config: {e}", "error")
        return {}

def ensure_log_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("Synthia log initialized.\n")

def main():
    ensure_log_file()
    config = load_config()

    log_level = config.get("log_level", "info")
    notifications = config.get("enable_notifications", False)

    log(f"Synthia is starting up...", log_level)
    log(f"Log level set to: {log_level}", log_level)
    log(f"Notifications enabled: {notifications}", log_level)

    # Main loop
    while True:
        log("Heartbeat – Synthia is running.", log_level)
        # Add your AI logic here in the future
        time.sleep(60)

if __name__ == "__main__":
    main()

import json
import time
import os
import threading
from datetime import datetime
from flask import Flask, render_template_string

LOG_PATH = "data/log.txt"
CONFIG_PATH = "/data/options.json"

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Synthia Status</title>
  <style>
    body { background: #111; color: #eee; font-family: sans-serif; padding: 2em; }
    h1 { color: #00e676; }
    .info { margin-bottom: 1em; }
    .logbox { background: #222; padding: 1em; border-radius: 4px; max-height: 300px; overflow-y: scroll; }
  </style>
</head>
<body>
  <h1>🧠 Synthia Status</h1>
  <div class="info"><strong>Log Level:</strong> {{ log_level }}</div>
  <div class="info"><strong>Notifications Enabled:</strong> {{ enable_notifications }}</div>
  <div class="info"><strong>Last Run:</strong> {{ last_run }}</div>
  <h2>Recent Logs</h2>
  <div class="logbox"><pre>{{ logs }}</pre></div>
</body>
</html>
"""

state = {
    "log_level": "info",
    "enable_notifications": False,
    "last_run": "Never"
}

def log(msg, level="info"):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] [{level.upper()}] {msg}"
    print(entry)  # <-- Required for add-on log tab
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            state["log_level"] = config.get("log_level", "info")
            state["enable_notifications"] = config.get("enable_notifications", False)
    except Exception as e:
        log(f"Error loading config: {e}", "error")

def background_loop():
    log("Background logic starting up...")
    while True:
        state["last_run"] = datetime.now().isoformat()
        log("Synthia heartbeat — I am alive.", state["log_level"])
        time.sleep(60)

@app.route("/")
def index():
    logs = ""
    try:
        with open(LOG_PATH) as f:
            logs = "\n".join(f.readlines()[-20:])  # Show last 20 lines
    except:
        logs = "Log file not found."
    return render_template_string(HTML,
                                  log_level=state["log_level"],
                                  enable_notifications=state["enable_notifications"],
                                  last_run=state["last_run"],
                                  logs=logs)

def main():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("Synthia log initialized.\n")

    load_config()

    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=8099)

if __name__ == "__main__":
    main()

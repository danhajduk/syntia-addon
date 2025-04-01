import json
import time
import os
import threading
from datetime import datetime
from flask import Flask, render_template, request

from utils import log
from openai_utils import run_openai_test
from assistant import SynthiaAssistant


LOG_PATH = "data/log.txt"
CONFIG_PATH = "/data/options.json"

app = Flask(__name__)
state = {
    "log_level": "info",
    "enable_notifications": False,
    "last_run": "Never"
}

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            state["log_level"] = config.get("log_level", "info")
            state["enable_notifications"] = config.get("enable_notifications", False)
            return config
    except Exception as e:
        log(f"Error loading config: {e}", "error")
        return {}

def ensure_log_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("Synthia log initialized.\n")

def background_loop():
    log("Background logic starting up...")
    while True:
        state["last_run"] = datetime.now().isoformat()
        log("Synthia heartbeat — I am alive.", state["log_level"])
        time.sleep(60)

@app.route("/")
def main_page():
    return render_template("main.html", active_page="main")

@app.route("/status")
def status_page():
    logs = ""
    try:
        with open(LOG_PATH) as f:
            logs = "\n".join(f.readlines()[-20:])
    except:
        logs = "Log file not found."
    return render_template(
        "status.html",
        log_level=state["log_level"],
        enable_notifications=state["enable_notifications"],
        last_run=state["last_run"],
        logs=logs,
        active_page="status"
    )

@app.route("/testing", methods=["GET", "POST"])
def testing_page():
    response = None
    prompt = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            config = load_config()
            api_key = config.get("openai_api_key", "")
            assistant_id = config.get("assistant_id", "")
            assistant = SynthiaAssistant(api_key, assistant_id)
            response = assistant.run(prompt)

    return render_template(
        "testing.html",
        prompt=prompt,
        response=response,
        active_page="testing"
    )

def main():
    ensure_log_file()
    config = load_config()

    # run_openai_test(
    #     config.get("openai_api_key", ""),
    #     config.get("assistant_id", "")
    # )

    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=8099)

if __name__ == "__main__":
    main()

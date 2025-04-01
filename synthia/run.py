import json
import time
import os
import threading
from datetime import datetime
from flask import Flask, render_template, request

from utils import log
from openai_utils import run_openai_test
from assistant import SynthiaAssistant
from usage import get_usage


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

    config = load_config()
    api_key = config.get("openai_api_key", "")
    usage = get_usage(api_key)

    # Optional: read cached last run time
    last_run_file = "data/last_run.txt"
    last_run = "Never"
    if os.path.exists(last_run_file):
        with open(last_run_file) as f:
            last_run = f.read().strip()

    return render_template(
        "status.html",
        log_level=state["log_level"],
        enable_notifications=state["enable_notifications"],
        last_run=last_run,
        logs=logs,
        usage=usage,
        active_page="status"
    )

@app.route("/testing", methods=["GET", "POST"])
def testing_page():
    response = None
    prompt = None
    thinking = False

    if request.method == "POST":
        thinking = True
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            config = load_config()
            api_key = config.get("openai_api_key", "")
            assistant_id = config.get("assistant_id", "")
            assistant = SynthiaAssistant(api_key, assistant_id)
            response = assistant.run(prompt)
            thinking = False

    return render_template(
        "testing.html",
        prompt=prompt,
        response=response,
        thinking=thinking,
        active_page="testing"
    )

@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    settings_file = "data/user_settings.json"
    settings = {"personality": "default", "reuse_thread": False}
    usage = None

    # Load existing settings
    if os.path.exists(settings_file):
        with open(settings_file) as f:
            settings.update(json.load(f))

    if request.method == "POST":
        settings["personality"] = request.form.get("personality", "default")
        settings["reuse_thread"] = "reuse_thread" in request.form
        with open(settings_file, "w") as f:
            json.dump(settings, f)

    # Optional: fake usage stats for now
    usage = {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579,
    }

    return render_template("settings.html", settings=settings, usage=usage, active_page="settings")

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

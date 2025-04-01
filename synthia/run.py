import json
import time
import os
import threading
from datetime import datetime
from flask import Flask, render_template, request

from utils import log
from assistant import SynthiaAssistant
from usage import get_usage

LOG_PATH = "data/log.txt"
CONFIG_PATH = "/data/options.json"
SETTINGS_PATH = "data/user_settings.json"

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
    except Exception as e:
        logs = "Log file not found."
        log(f"[STATUS] Could not read log file: {e}", "warning")

    config = load_config()
    usage = {
        "total_tokens": "Unavailable",
        "start_date": None,
        "end_date": None
    }

    # Load saved settings to get admin API key
    config = load_config()
    admin_key = config.get("admin_api_key")

    if admin_key:
        try:
            usage = get_usage(admin_key)
        except Exception as e:
            log(f"[STATUS] Error getting usage from OpenAI: {e}", "error")
    else:
        log(f"[STATUS] No admin API key set. Skipping usage fetch.", "info")

    # Read last assistant request time
    last_run = "Never"
    try:
        with open("data/last_run.txt") as f:
            last_run = f.read().strip()
    except Exception as e:
        log(f"[STATUS] Could not read last_run.txt: {e}", "warning")

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
    settings = {
        "personality": "default",
        "reuse_thread": False,
        "admin_api_key": ""
    }

    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            settings.update(json.load(f))

    if request.method == "POST":
        settings["personality"] = request.form.get("personality", "default")
        settings["reuse_thread"] = "reuse_thread" in request.form
        settings["admin_api_key"] = request.form.get("admin_api_key", "")
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f)

    try:
        admin_key = settings.get("admin_api_key")
        if admin_key:
            usage = get_usage(admin_key)
    except Exception as e:
        log(f"Failed to fetch usage: {e}", "error")

    return render_template(
        "settings.html",
        settings=settings,
        usage=usage,
        active_page="settings"
    )

def main():
    ensure_log_file()
    config = load_config()

    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=8099)

if __name__ == "__main__":
    main()

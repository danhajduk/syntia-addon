from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import json
from assistant import SynthiaAssistant
from usage import  get_costs
from utils import log

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_page": "main"})

@app.get("/status", response_class=HTMLResponse)
async def status_page(request: Request):
    logs = ""
    try:
        with open(LOG_PATH) as f:
            logs = "\n".join(f.readlines()[-20:])
    except Exception as e:
        logs = "Log file not found."
        log(f"[STATUS] Could not read log file: {e}", "warning")

    config = load_config()
    admin_key = config.get("admin_api_key")

    usage = {
        "total_tokens": "Unavailable",
        "input_tokens": 0,
        "output_tokens": 0,
        "start_time": None,
        "end_time": None
    }

    costs = {
        "total_cost": "Unavailable",
        "currency": "USD",
        "start_time": None,
        "end_time": None
    }

    if admin_key:
        try:
            usage = get_completions_usage(admin_key)
        except Exception as e:
            log(f"[STATUS] Error getting usage: {e}", "error")

        try:
            costs = get_costs(admin_key)
        except Exception as e:
            log(f"[STATUS] Error getting costs: {e}", "error")
    else:
        log(f"[STATUS] No admin API key set in config. Skipping usage and cost fetch.", "info")

    last_run = "Never"
    try:
        with open("data/last_run.txt") as f:
            last_run = f.read().strip()
    except Exception as e:
        log(f"[STATUS] Could not read last_run.txt: {e}", "warning")

    return templates.TemplateResponse("status.html", {
        "request": request,
        "log_level": state["log_level"],
        "enable_notifications": state["enable_notifications"],
        "last_run": last_run,
        "logs": logs,
        "usage": usage,
        "costs": costs,
        "active_page": "status"
    })

@app.get("/testing", response_class=HTMLResponse)
async def testing_page(request: Request):
    return templates.TemplateResponse("testing.html", {"request": request, "response": None, "prompt": "", "active_page": "testing"})

@app.post("/testing", response_class=HTMLResponse)
async def testing_post(request: Request, prompt: str = Form(...)):
    config = load_config()
    api_key = config.get("openai_api_key")
    assistant_id = config.get("openai_assistant_id")
    response_text = ""

    if api_key and assistant_id:
        assistant = SynthiaAssistant(api_key, assistant_id)
        response_text = assistant.run(prompt)

    try:
        with open("data/last_run.txt", "w") as f:
            from datetime import datetime
            f.write(datetime.now().isoformat())
    except:
        pass

    return templates.TemplateResponse("testing.html", {
        "request": request,
        "response": response_text,
        "prompt": prompt,
        "active_page": "testing"
    })

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8099, reload=False)

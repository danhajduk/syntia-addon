from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
import threading
import time
from utils import log

# FastAPI app
app = FastAPI()

# Serve static HTML/JS/CSS files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/api/chat")
async def chat_api(prompt: str = Form(...)):
    try:
        # Load API key and assistant ID from saved settings
        if os.path.exists("data/user_settings.json"):
            with open("data/user_settings.json") as f:
                settings = json.load(f)
                api_key = settings.get("openai_api_key")
                assistant_id = settings.get("assistant_id")
        else:
            return JSONResponse({"error": "Missing settings"}, status_code=400)

        if not api_key or not assistant_id:
            return JSONResponse({"error": "Missing API key or Assistant ID"}, status_code=400)

        assistant = SynthiaAssistant(api_key, assistant_id)
        reply = assistant.run(prompt)
        return {"reply": reply}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)



def background_loop():
    log("Background logic starting up...", "info")
    while True:
        log("Synthia heartbeat — I am alive.", "debug")
        time.sleep(60)

# Start background logic
threading.Thread(target=background_loop, daemon=True).start()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8099, reload=True)

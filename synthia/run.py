from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import threading
import time
from utils import log

# FastAPI app
app = FastAPI()

# Serve static HTML/JS/CSS files
app.mount("/", StaticFiles(directory="static", html=True), name="static")



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

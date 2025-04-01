from assistant import SynthiaAssistant
from utils import log

def run_openai_test(api_key, assistant_id):
    if not api_key or not assistant_id:
        log("Missing OpenAI credentials – skipping assistant test.", "warning")
        return

    try:
        assistant = SynthiaAssistant(api_key, assistant_id)
        result = assistant.run("Tell me something cool about ducks.")
        log(f"🧠 Assistant response: {result}")
    except Exception as e:
        log(f"❌ Assistant failed: {e}", "error")

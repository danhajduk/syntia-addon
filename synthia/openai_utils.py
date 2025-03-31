import openai
from run import log  # Importing your shared logging function

def run_openai_test(api_key):
    if not api_key:
        log("OpenAI API key not set — skipping OpenAI test.", "warning")
        return

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Tell me a joke about ducks"}
            ]
        )
        answer = response['choices'][0]['message']['content']
        log(f"🧠 OpenAI replied: {answer}")
    except Exception as e:
        log(f"❌ OpenAI request failed: {e}", "error")

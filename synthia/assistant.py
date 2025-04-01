# assistant.py
import time
import openai
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SynthiaAssistant:
    def __init__(self, api_key, assistant_id):
        self.client = openai.OpenAI(api_key=api_key)
        self.assistant_id = assistant_id

    def run(self, prompt):
        try:
            # Create a new thread each time, or reuse one if you want context
            thread = self.client.beta.threads.create()
            
            # Add the user prompt
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt,
            )

            # Run the assistant
            run = self.client.beta.threads.runs.create(
                assistant_id=self.assistant_id,
                thread_id=thread.id,
            )

            # Wait for the run to complete
            while True:
                status = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if status.status == "completed":
                    break
                elif status.status == "failed":
                    logger.error("Assistant run failed.")
                    return "Sorry, I couldn't process that."
                time.sleep(1)

            # Get the assistant's reply
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            with open("data/last_run.txt", "w") as f:
                f.write(datetime.now().isoformat())            
            return messages.data[0].content[0].text.value.strip()

        except Exception as e:
            logger.error(f"Assistant error: {e}")
            return "An error occurred while talking to the assistant."

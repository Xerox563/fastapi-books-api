from openai import OpenAI
from dotenv import load_dotenv
import os 
import time
from dependencies.config import client


# system Prompts
SYSTEM_PROMPTS = {
    "friendly": "You are a friendly assistant. Be warm!",
    "technical": "You are a technical expert. Be precise!",
}

class OpenAIBot:

    def __init__(self):
        self.question = "What is FastAPI?"
        self.max_retries = 3

    def call_api_with_retry(self, system_prompt: str):

        for attempt in range(self.max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # or your OpenRouter model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": self.question}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )

                return response.choices[0].message.content

            except Exception as e:
                wait_time = 2 ** attempt

                if attempt < self.max_retries - 1:
                    print(f"Error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Failed after {self.max_retries} attempts: {e}")
                    return None
                
    def test(self):
        print("="*80)
        print("OPENAI BOT - Error Handling")
        print("="*80)

        for name, prompt in SYSTEM_PROMPTS.items():
            print(f"\n--- {name} ---")

            response = self.call_api_with_retry(prompt)

            if response:
                print(response)
            else:
                print("Failed") 

  

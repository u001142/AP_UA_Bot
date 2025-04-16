
import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "openrouter/codellama-70b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(BASE_URL, headers=headers, json=body)
    data = response.json()
    return data["choices"][0]["message"]["content"]

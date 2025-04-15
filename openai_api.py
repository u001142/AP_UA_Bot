import os
import requests

def ask_ai(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if r.status_code == 200:
        return r.json()['choices'][0]['message']['content']
    return "Вибач, щось пішло не так з AI-відповіддю."
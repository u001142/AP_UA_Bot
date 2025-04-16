import os
import requests

def ask_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    json = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "Помилка запиту до ШІ. Спробуйте пізніше."

import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-4"

def ask_ai(prompt: str) -> str:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Виникла помилка при зверненні до AI: {e}"

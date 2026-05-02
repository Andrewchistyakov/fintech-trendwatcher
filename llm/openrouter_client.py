import requests
import os
from keys import OPENROUTER_KEY

URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "qwen/qwen3.6-35b-a3b" # "qwen/qwen3.6-flash"  


def generate(prompt: str) -> str:
    response = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Ты аналитик финтех-рынка. Пиши кратко и по делу."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
        }
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
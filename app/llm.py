
import os, json, requests
from typing import Dict

class LLM:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.api_key = os.getenv("OPENAI_API_KEY")

    def chat(self, system: str, user: str) -> str:
        # Minimal OpenAI-compatible client; easy to swap or point to a local server
        if not self.api_key and self.provider in ("openai", "http"):
            # Fallback: local echo so examples still run without a key
            return f"[LLM unavailable] " + user[:600]
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload: Dict = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()

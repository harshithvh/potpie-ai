"""
Grok LLM adapter (replaces Claude).
"""

import requests
import json
from app.interfaces.ai_model import ILanguageModel

class GrokLanguageModel(ILanguageModel):
    def __init__(self, api_key: str, model: str = "grok-1"):
        self.api_key = api_key
        self.model = model

    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type):
        url = "https://api.grok.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
        }
        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
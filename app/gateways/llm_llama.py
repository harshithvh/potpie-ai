"""
Llama LLM adapter (example: using llama.cpp server).
"""

import requests
import json
from app.interfaces.ai_model import ILanguageModel

class LlamaLanguageModel(ILanguageModel):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type):
        payload = {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }
        resp = requests.post(self.endpoint, json=payload)
        resp.raise_for_status()
        content = resp.json()["content"]
        return json.loads(content)
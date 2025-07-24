"""
OpenAI LLM adapter.
"""

import openai
from app.interfaces.ai_model import ILanguageModel

class OpenAILanguageModel(ILanguageModel):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
        )
        content = response.choices[0].message["content"]
        # Assume the LLM returns a JSON list of issues
        import json
        return json.loads(content)
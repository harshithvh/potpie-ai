"""
OpenRouter LLM adapter.
"""

import instructor
from openai import OpenAI
from typing import TypeVar
from logging import Logger
from app.interfaces.ai_model import ILanguageModel

# Generic type for Pydantic models
PydanticModel = TypeVar('PydanticModel')


class OpenRouterLanguageModel(ILanguageModel):
    def __init__(self, logger: Logger, api_key: str, model: str = "gpt-4o-mini"):
        self.logger = logger
        self.api_key = api_key
        self.model = model
        
        # Initialize OpenAI client with OpenRouter base URL
        self.openai = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        # Initialize OpenAI client withe Requesty base URL
        # self.openai = OpenAI(
        #     base_url="https://router.requesty.ai/v1",
        #     api_key=api_key
        # )
        
        # Initialize Instructor client for structured outputs
        self.client = instructor.from_openai(self.openai)

    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type):
        """
        Send a prompt and get a structured response using the specified Pydantic model.
        """
        try:
            
            response = self.client.chat.completions.create(
                model=self.model,
                response_model=response_type,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            return response
            
        except Exception as e:
            self.logger.error(f"Error making OpenRouter request: {e}")
            raise

    def sync_prompt_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a prompt and get a plain text response (without structured output).
        """
        try:
            
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            
            content = response.choices[0].message.content or ""
            return content
            
        except Exception as e:
            self.logger.error(f"Error making OpenRouter text request: {e}")
            raise
"""
Interface for language model adapters.
"""

from typing import Any

class ILanguageModel:
    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type: Any) -> Any:
        raise NotImplementedError
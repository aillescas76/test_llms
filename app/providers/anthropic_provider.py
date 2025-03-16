from typing import Optional
import anthropic
from app.providers.base_provider import BaseProvider
import os

class AnthropicProvider(BaseProvider):
    def __init__(self, config):
        self.client = anthropic.Anthropic(api_key=self.get_api_key())
        self.config = config

    def _generate_response_implementation(self, prompt: str) -> tuple[str, Optional[str]]:
        message = self.client.messages.create(
            model=self.config['model_name'],
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text, None

    @classmethod
    def get_api_key(cls):
        return os.getenv("ANTHROPIC_API_KEY")

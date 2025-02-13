from typing import Optional
from openai import OpenAI
from app.providers.base_provider import BaseProvider
import os
import logging

class OpenaiProvider(BaseProvider):
    def __init__(self, config):
        self.logger = logging.getLogger('OpenAIProvider')
        params = {
            "api_key": self.get_api_key(config)
        }
        if config.get("url"):
            params['base_url'] = config["url"]

        self.client = OpenAI(**params)
        self.config = config

    def generate_response(self, prompt: str) -> tuple[str, Optional[str]]:
        try:
            self.logger.info(f"Starting OpenAI API call - Model: {self.config['model_name']}")
            self.logger.debug(f"Full prompt content:\n{prompt[:500]}...")
            
            completion = self.client.chat.completions.create(
                model=self.config['model_name'],
                messages=[{"role": "user", "content": prompt}]
            )
            
            self.logger.info(f"OpenAI API call successful - Tokens used: {completion.usage.total_tokens}")
            return completion.choices[0].message.content, None
            
        except Exception as e:
            self.logger.error(f"OpenAI API Error: {str(e)}", exc_info=True)
            raise

    @classmethod
    def get_api_key(cls, config):
        key = config.get("key", "OPENAI_API_KEY")
        return os.getenv(key)

from typing import Optional
from app.providers.base_provider import BaseProvider
import os
import logging
import requests
import json

class DeepseekProvider(BaseProvider):
    def __init__(self, config):
        self.logger = logging.getLogger('DeepseekProvider')
        self.config = config

    def _generate_response_implementation(self, prompt: str) -> tuple[str, Optional[str]]:
        try:
            self.logger.info(f"Starting Deepseek API call - Model: {self.config['model_name']}")
            self.logger.debug(f"Full prompt content:\n{prompt[:500]}...")  # Log first 500 chars
            
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.get_api_key()}"
            }
            data = {
                "model": self.config['model_name'],
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(data))

            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Deepseek API call successful")
            message = result['choices'][0]['message']
            return message['content'], message.get('reasoning_content', None)
            
        except Exception as e:
            self.logger.error(f"Deepseek API Error: {str(e)}", exc_info=True)
            raise

    @classmethod
    def get_api_key(cls):
        return os.getenv("DEEPSEEK_API_KEY")

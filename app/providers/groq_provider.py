from typing import Optional, Tuple
import logging
from app.providers.base_provider import BaseProvider
from groq import Groq

class GroqProvider(BaseProvider):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("GroqProvider")
        # Initialize the Groq client
        self.client = Groq()

    def _generate_response_implementation(self, prompt: str) -> Tuple[str, Optional[str]]:
        """
        Generates a chat response using Groq's models.
        """
        # Build messages list for chat; adjust as needed.
        messages = [{"role": "user", "content": prompt}]
        # Set parameters either from config or default values.
        model = self.config.get("model_name", "mixtral-8x7b-32768")
        temperature = self.config.get("temperature", 1)
        max_completion_tokens = self.config.get("max_completion_tokens", 1024)
        top_p = self.config.get("top_p", 1)
        stream_output = self.config.get("stream", True)  # default to streaming if not defined

        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
                top_p=top_p,
                stream=stream_output,
                stop=None,
            )

            response_text = ""
            if stream_output:
                for chunk in completion:
                    response_text += chunk.choices[0].delta.content or ""
            else:
                # Assuming non-streaming output returns a similar structure
                response_text = completion.choices[0].message.content
            return response_text, None
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "", str(e)

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """
        Groq provider does not require an API key by default.
        """
        return None

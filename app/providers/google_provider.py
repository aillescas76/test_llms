from typing import Optional
import os
import logging
from app.providers.base_provider import BaseProvider
from google import genai
from google.genai import types

class GoogleProvider(BaseProvider):
    def __init__(self, config):
        self.logger = logging.getLogger("GoogleProvider")
        self.config = config
        self.client = genai.Client(api_key=self.get_api_key())

    def _generate_response_implementation(self, prompt: str) -> tuple[str, Optional[str]]:
        try:
            self.logger.info("Starting Google API call")
            # Prepare the API call components using the prompt
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ]
            generate_content_config = types.GenerateContentConfig(
                temperature=1,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_modalities=["text"],
                response_mime_type="text/plain",
            )
            response_text = ""
            reasoning = None  # Optionally fill in any reasoning if available

            for chunk in self.client.models.generate_content_stream(
                model=self.config.get("model_name", "gemini-2.0-flash-exp-image-generation"),
                contents=contents,
                config=generate_content_config,
            ):
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                candidate = chunk.candidates[0]
                if candidate.content.parts[0].inline_data:
                    self.logger.info("Encountered inline binary data; skipping it")
                    continue
                else:
                    response_text += candidate.content.parts[0].text

            return response_text, reasoning
        except Exception as e:
            self.logger.error(f"Google API Error: {e}", exc_info=True)
            raise

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        return os.getenv("GEMINI_API_KEY")

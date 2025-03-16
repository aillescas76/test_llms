from abc import ABC, abstractmethod
from typing import Optional, Tuple
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()  # Load environment variables

class BaseProvider(ABC):
    def generate_response(self, prompt: str) -> Tuple[str, Optional[str]]:
        start_time = time.perf_counter()
        response = self._generate_response_implementation(prompt)
        elapsed_time = time.perf_counter() - start_time
        prompt_length = len(prompt)
        # Assume each provider sets self.config; fallback to 'unknown' if missing.
        model_name = self.config.get("model_name", "unknown") if hasattr(self, "config") else "unknown"
        logging.getLogger(__name__).info(
            f"Model: {model_name}, prompt length: {prompt_length}, generation time: {elapsed_time:.2f} seconds"
        )
        return response
        
    @abstractmethod
    def _generate_response_implementation(self, prompt: str) -> Tuple[str, Optional[str]]:
        pass

    @classmethod
    @abstractmethod
    def get_api_key(cls) -> Optional[str]:
        pass

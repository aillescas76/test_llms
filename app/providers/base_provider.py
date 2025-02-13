from abc import ABC, abstractmethod
from typing import Optional, Tuple
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

class BaseProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> Tuple[str, Optional[str]]:
        pass

    @classmethod
    @abstractmethod
    def get_api_key(cls) -> Optional[str]:
        pass

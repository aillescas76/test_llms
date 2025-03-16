from typing import Optional
from app.providers import AnthropicProvider, OpenaiProvider, DeepseekProvider, GoogleProvider
from app.providers.groq_provider import GroqProvider
from app.models.config import load_config

class ProviderManager:
    PROVIDER_MAP = {
        "anthropic": AnthropicProvider,
        "openai": OpenaiProvider,
        "deepseek": DeepseekProvider,
        "google": GoogleProvider,
        "groq": GroqProvider,
    }

    def __init__(self, config):
        self.providers = {}
        for model in config['models']:
            provider_class = self.PROVIDER_MAP[model['provider']]
            self.providers[model['name']] = provider_class(model['config'])

    def get_response(self, model_name: str, prompt: str) -> tuple[str, Optional[str]]:
        provider = self.providers.get(model_name)
        if not provider:
            raise ValueError(f"Provider for {model_name} not found")
        return provider.generate_response(prompt)
        
    @staticmethod
    def get_summary_provider_manager() -> "ProviderManager":
        config = load_config()
        for model in config.get("models", []):
            # Look for the first model with summary=True in its config.
            if model.get("config", {}).get("summary") is True:
                return ProviderManager({"models": [model]})
        raise ValueError("No summary provider found in config.")

from typing import Optional
from app.providers import AnthropicProvider, OpenaiProvider, DeepseekProvider

class ProviderManager:
    PROVIDER_MAP = {
        "anthropic": AnthropicProvider,
        "openai": OpenaiProvider,
        "deepseek": DeepseekProvider
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

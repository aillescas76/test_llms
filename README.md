# LLM Chat Interface

## Overview

The LLM Chat Interface is a Python application that lets users interact with multiple large language model providers through a clean graphical interface built with Qt. The application supports providers such as Anthropic, OpenAI, and Deepseek. Each provider is integrated as a separate component that adheres to a common interface defined by `BaseProvider`. The modular architecture makes it easy to add or update providers.

## Directory Structure

```
.
├── app
│   ├── __init__.py
│   ├── main.py                  # Application entry point
│   ├── models
│   │   ├── config.py            # Configuration loader
│   │   └── schemas.py           
│   ├── providers                # Provider implementations
│   │   ├── __init__.py
│   │   ├── base_provider.py     # Abstract base class for providers
│   │   ├── anthropic_provider.py# Anthropic provider implementation
│   │   ├── deepseek_provider.py # Deepseek provider implementation
│   │   └── openai_provider.py   # OpenAI provider implementation
│   ├── services
│   │   ├── __init__.py
│   │   └── provider_manager.py  # Manages provider instantiation and response flow
│   ├── views
│   │   ├── __init__.py
│   │   ├── main_window.py       # Main window and Qt thread workers
│   │   └── widgets              # Custom UI widgets (input, model selection, result display)
│   │       ├── __init__.py
│   │       ├── input_widget.py
│   │       ├── model_selection.py
│   │       └── result_widget.py
├── config
│   └── models_config.yaml       # YAML file with models configuration
├── .gitignore
├── requirements.txt             # List of dependencies
└── llm_accesss_examples.md      # Example usages for accessing the LLM
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**

   Make sure you have Python 3.8+ installed. Create a virtual environment if desired, then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys & Settings:**

   - Update `config/models_config.yaml` with your provider-specific configurations.
   - Set the environment variables, if needed, for API keys used in the providers.

4. **Run the Application:**

   Execute the main application script:

   ```bash
   python -m app.main
   ```

## Adding/Modifying Providers

- Each provider is defined under `app/providers/`. They inherit from `BaseProvider` and implement the `generate_response` method along with a class method to fetch API keys.
- The `ProviderManager` in `app/services/provider_manager.py` maps model names (e.g., "anthropic", "openai", "deepseek") to their corresponding providers. Update this mapping if you add a new provider.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make changes and ensure tests pass.
4. Submit a pull request describing your changes.

## License

[Include your license information here.]

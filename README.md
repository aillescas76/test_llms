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

## Installing Qt6

For the graphical interface, this application requires Qt6. Please follow the instructions below for your platform:

**Windows:**
 - Download the official Qt6 installer from [Qt Downloads](https://www.qt.io/download-qt-installer) and follow the installation instructions.
 - Alternatively, if you only need the Python bindings, install PySide6 (which supports Qt6) via pip:
   ```bash
   pip install PySide6
   ```

**macOS:**
 - Install Qt6 using Homebrew:
   ```bash
   brew install qt6
   ```
 - Or download the installer from [Qt Downloads](https://www.qt.io/download-qt-installer).

**Linux (Ubuntu/Debian-based):**
 - Update your package list and install the Qt6 development packages:
   ```bash
   sudo apt update
   sudo apt install qt6-base-dev
   ```
 - Additionally, install the xcb-cursor library which is required by Qt 6.5.0 and later:
   ```bash
   sudo apt install libxcb-cursor0
   ```
   
   # Installing libxcb-cursor0 ensures that the Qt xcb platform plugin loads correctly.
 - If you encounter errors like:
   
   ```
   undefined symbol: _ZN5QFont11tagToStringEj, version Qt_6
   ```
   
   then it is likely that your system's Qt6 libraries are incompatible with the version expected by PyQt6. To resolve this:
   
   - Ensure you are using PyQt6 installed via pip—which bundles compatible Qt6 libraries—in your virtual environment:
     ```bash
     pip install --upgrade PyQt6
     ```
   
   - If conflicts persist (for example due to system-wide Qt6 libraries), you may need to adjust your environment so that the PyQt6 libraries are preferred. For example:
     ```bash
     export LD_LIBRARY_PATH="<path-to-your-venv>/lib/python3.10/site-packages/PyQt6:$LD_LIBRARY_PATH"
     ```
   
   - Alternatively, consider removing or disabling conflicting system-installed Qt6 libraries.
 - If you encounter errors like:
   
   ```
   undefined symbol: _ZN5QFont11tagToStringEj, version Qt_6
   ```
   
   then it is likely that your system's Qt6 libraries are incompatible with the version expected by PyQt6. To resolve this:
   
   - Ensure you are using PyQt6 installed via pip—which bundles compatible Qt6 libraries—in your virtual environment:
     ```bash
     pip install --upgrade PyQt6
     ```
   
   - If conflicts persist (for example due to system-wide Qt6 libraries), you may need to adjust your environment so that the PyQt6 libraries are preferred. For example:
     ```bash
     export LD_LIBRARY_PATH="<path-to-your-venv>/lib/python3.10/site-packages/PyQt6:$LD_LIBRARY_PATH"
     ```
   
   - Alternatively, consider removing or disabling conflicting system-installed Qt6 libraries.
 - For other Linux distributions, consult your package manager or use the official installer from [Qt Downloads](https://www.qt.io/download-qt-installer).

4. **Run the Application:**

   Execute the main application script:

   ```bash
   python -m app.main
   ```

5. **Install mpv for Audio Streaming:**

   The voice feedback functionality requires [mpv](https://mpv.io/) to stream audio. If you encounter an error "mpv not found", install it as follows:

   **macOS:**
   Install via Homebrew:
   ```bash
   brew install mpv
   ```

   **Linux and Windows:**
   Download and install it from the [mpv website](https://mpv.io/).

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

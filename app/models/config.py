import yaml

def load_config():
    with open('config/models_config.yaml') as f:
        return yaml.safe_load(f)

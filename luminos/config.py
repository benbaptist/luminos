import os
import yaml

from luminos.models.openai.gpt35 import GPT35  
from luminos.models.anthropic import BaseAnthropic
from luminos.models.openai.gpt4 import GPT4

def get_model_class(provider, name):
    model_map = {
        "openai": {
            "gpt-3.5-turbo": GPT35,
            "gpt-4-0125-preview": GPT4
        },
        "anthropic": {
            "claude3": BaseAnthropic
        }
    }
    try:
        return model_map[provider][name]
    except KeyError:
        raise ModelNotFoundException(f"Model '{name}' with provider '{provider}' not found")
    
def merge_configs(default, existing):
    merged = existing.copy()
    for key, value in default.items():
        if isinstance(value, dict):
            merged[key] = merge_configs(value, merged.get(key, {}))
        else:
            merged.setdefault(key, value)
    return merged

class Config:
    def __init__(self):
        self.config_path = os.path.expanduser('~/.config/luminos/config.yaml')
        self.settings = self.load_config()

    def load_config(self):
        default_full_config = {
            'api_key': {
                'openai': None,
                'anthropic': None
            },
            'model': {
                'name': 'gpt-4-0125-preview',
                'provider': "openai"
            }
        }

        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as config_file:
                yaml.dump(default_full_config, config_file, default_flow_style=False)

            print('Default config generated at:', self.config_path)
            return None
        else:
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)

            config = merge_configs(default_full_config, config)

        return config

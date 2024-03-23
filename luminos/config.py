import os
import yaml

class Config:
    def __init__(self):
        self.config_path = os.path.expanduser('~/.config/luminos/config.yaml')
        self.settings = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as config_file:
                default_config = {
                    'OPENAI_API_KEY': None,
                    'PERSIST_CONVO': True,
                    'LLM_MODEL': 'gpt-4-0125-preview' # Default LLM Model
                }
                yaml.dump(default_config, config_file)
            print('Default config generated at:', self.config_path)
        with open(self.config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        return config
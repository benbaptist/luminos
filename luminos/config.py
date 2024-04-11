import os
import yaml

class Config:
    def __init__(self):
        self.config_path = os.path.expanduser('~/.config/luminos/config.yaml')
        self.settings = self.load_config()

    def load_config(self):
        default_full_config = {
            'api': {
                'openai_key': None,
                'anthropic_key': None
            },
            'model': {
                'name': 'gpt-4-0125-preview'
            }
        }

        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as config_file:
                yaml.dump(default_full_config, config_file, default_flow_style=False)
            print('Default config generated at:', self.config_path)
        else:
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)

            # Merge any new parameters from default_full_config into existing config
            for key, value in default_full_config.items():
                if isinstance(value, dict):
                    config.setdefault(key, {}).update(value)
                else:
                    config.setdefault(key, value)

            with open(self.config_path, 'w') as config_file:
                yaml.dump(config, config_file, default_flow_style=False)

        return config
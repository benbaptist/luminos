from typing import Optional
import os
import logging
import sys

from .config import Config
from .logic import Logic
from .input import Input
from .logger import logger
from .exceptions import ModelNotFoundException

class App:
    def __init__(self) -> None:
        self.config = Config()
        if not self.config.settings:
            print("Config file created at ~/.config/luminos/config.yaml. Please edit it before running Luminos again.")
            sys.exit(0)

    def setup_logging(self, verbose: bool) -> None:
        LOG_DIRECTORY = os.path.expanduser('~/.config/luminos/logs')

        os.makedirs(LOG_DIRECTORY, exist_ok=True) # Ensure log directory exists
        LOG_FILE = os.path.join(LOG_DIRECTORY, 'luminos.log')

        file_handler = logging.FileHandler(LOG_FILE)
        console_handler = logging.StreamHandler()
        
        level = logging.DEBUG if verbose else logging.INFO
        logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    def start(self, permissive: bool, directory: Optional[str], model_name: Optional[str] = None, provider: Optional[str] = None, api_key: Optional[str] = None) -> None:
        model_name = model_name or self.config.settings.get("defaults", {}).get("model")
        provider = provider or self.config.settings.get("defaults", {}).get("provider")

        if not model_name or not provider:
            logger.error("Default model name and/or provider not specified in configuration. Exiting.")
            sys.exit(1)

        try:
            model_class = self.config.get_model_class(provider, model_name)
        except ModelNotFoundException as e:
            logger.error(f"Error getting model class: {e}")
            sys.exit(1)

        self.logic = Logic(self, model_class=model_class, api_key=api_key)

        input_handler = Input(permissive=permissive, directory=directory, logic=self.logic)
        input_handler.start()

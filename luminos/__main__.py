import pkg_resources
from typing import Optional
import click
import logging
import os

from luminos.logger import logger
from luminos.config import Config
from luminos.logic import Logic
from luminos.input import Input
from luminos.exceptions import ModelNotFoundException
import sys

class Main:
    def __init__(self) -> None:
        self.config = Config()
        if not self.config.settings:
            print("Config file created at ~/.config/luminos/config.yaml. Please edit it before running Luminos again.")
            return

    def setup_logging(self, verbose: bool) -> None:
        LOG_DIRECTORY = os.path.expanduser('~/.config/luminos/logs')
        LOG_FILE = os.path.join(LOG_DIRECTORY, 'luminos.log')

        if verbose:
            logger.setLevel(logging.DEBUG)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        else:
            logger.setLevel(logging.INFO)

    def start(self, permissive: bool, directory: str, model_name: Optional[str] = None, provider: Optional[str] = None, api_key: Optional[str] = None) -> None:
        model_name = model_name or self.config.settings["defaults"].get('model')
        provider = provider or self.config.settings["defaults"].get('provider')
        
        if model_name is None or provider is None:
            logger.error("Model_name and/or provider is None. Exiting the program.")
            sys.exit(1)
        
        try:
            model_class = self.config.get_model_class(provider, model_name)
        except ModelNotFoundException as e:
            logger.error(f"Error getting model class: {e}")
            return

        self.logic = Logic(self, model_class=model_class, api_key=api_key or self.config.settings.get('api_key'))
        input_handler = Input(permissive=permissive, directory=directory, logic=self.logic)
        input_handler.start()

def main() -> None:
    try:
        __version__ = pkg_resources.get_distribution("luminos").version
    except pkg_resources.DistributionNotFound:
        __version__ = "unknown"

    logger.info(f"Luminos version: {__version__}")
    app = Main()
    app.setup_logging(verbose=True)  # Set verbose to True by default
    app.start(permissive=False, directory='.')

if __name__ == "__main__":
    main()

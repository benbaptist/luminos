from typing import Optional
import click
import logging
import os

from luminos.logger import logger

from luminos.config import Config
from luminos.logic import Logic
from luminos.input import Input

class Main:
    def __init__(self) -> None:
        self.config = Config()

        logger.info("Howdy")

    def start(self, permissive: bool, directory: str, model_str: str, api_key: Optional[str]) -> None: 
        model = None
        if model_str:
            try:
                provider, name = model_str.split("/")
                model = (provider, name)
            except ValueError:
                raise Exception(f"Invalid provider/model: {model_str}")

        self.logic = Logic(self, model=model, api_key=api_key)

        input_handler = Input(permissive=permissive, directory=directory, logic=self.logic)
        input_handler.start()

def main() -> None:
    @click.command()
    @click.option('--permissive', '-p', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
    @click.option('--model', '-m', help='Model provider and name in format provider/model_name')
    @click.option('--api-key', '-k', help='API key for model provider') 
    @click.option('--verbose', '-v', is_flag=True, default=False, help='Spit out more information when making requests') 
    @click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
    def cli(permissive: bool, verbose: bool, model: str, api_key: Optional[str], directory: Optional[str] = '.'):
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
        
        app = Main()
        app.start(permissive, directory, model, api_key)

    cli()

if __name__ == "__main__":
    main()
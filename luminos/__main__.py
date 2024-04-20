from typing import Optional
import click

from luminos.config import Config
from luminos.logic import Logic
from luminos.input import start_user_interaction

class Main:
    def __init__(self) -> None:
        self.config = Config()
        self.logic = Logic(self)

    def start(self, permissive: bool, directory: str, model: str, api_key: Optional[str]) -> None: 
        self.config.model = model
        if api_key:
            self.config.api_key = api_key
        start_user_interaction(permissive, directory, self.logic)

def main() -> None:
    @click.command()
    @click.option('--permissive', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
    @click.option('--model', '-m', required=True, help='Model provider and name in format provider/model_name')
    @click.option('--api-key', '-k', help='API key for model provider') 
    @click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
    def cli(permissive: bool, model: str, api_key: Optional[str], directory: Optional[str] = '.') -> None:
        app = Main()
        app.start(permissive, directory, model, api_key)

    cli()

if __name__ == "__main__":
    main()
from typing import Optional
import click

from luminos.config import Config
from luminos.logic import Logic
from luminos.input import start_user_interaction

class Main:
    def __init__(self) -> None:
        self.config = Config()
        self.logic = Logic(self)

    def start(self, permissive: bool, directory: str) -> None:
        start_user_interaction(permissive, directory, self.logic)

def main() -> None:
    @click.command()
    @click.option('--permissive', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
    @click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
    def cli(permissive: bool, directory: Optional[str] = '.') -> None:
        app = Main()
        app.start(permissive, directory)

    cli()

if __name__ == "__main__":
    main()
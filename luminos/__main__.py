"""Entry point for Luminos CLI"""

import click
from luminos.config import Config
from luminos.logic import Logic
from luminos.input import Input

class LuminosCLI:
    def __init__(self):
        self.config = Config()
        self.logic = Logic(self)
        self.input = Input(self.logic)

    def run(self, permissive, directory):
        self.input.start_interaction(permissive, directory)

@click.command()
@click.option('--permissive', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
@click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
def main(permissive, directory='.'):
    cli = LuminosCLI()
    cli.run(permissive, directory)

if __name__ == "__main__":
    main()
from luminos.logic import Logic
from luminos.config import Config
from luminos.input import get_user_input, start_user_interaction

import click

class Main:
    def __init__(self):
        self.config = Config()
        self.logic = Logic(self)

    def start(self, permissive, directory):
        start_user_interaction(permissive, directory, self.logic)


def main():
    @click.command()
    @click.option('--permissive', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
    @click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
    def cli(permissive, directory='.'):
        app = Main()
        app.start(permissive, directory)

    cli()

if __name__ == "__main__":
    main()

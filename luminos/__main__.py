import click
from luminos.core import Core
import os
import sys
import time
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

# Configure key bindings for advanced input handling
bindings = KeyBindings()

# Bind Shift+Enter to insert a newline instead of submitting
@bindings.add('enter', shift=True)
def _(event):
    event.current_buffer.insert_text('\n')

class Main:
    def __init__(self):
        self.core = Core()

    def start(self, always_grant_permission, directory):
        # Apply the always grant permission setup
        if always_grant_permission:
            os.environ['ALWAYS_GRANT_PERMISSION'] = '1'
        else:
            os.environ['ALWAYS_GRANT_PERMISSION'] = '0'

        # Change to the specified directory if provided
        if directory:
            os.chdir(directory)

        while True:
            try:
                user_input = prompt("<user> ", multiline=True, key_bindings=bindings)
            except EOFError:
                print("")
                continue
            except KeyboardInterrupt:
                break

            with open(".luminos_history", "a") as f:
                f.write(f"{time.time()} {user_input}\n")

            self.core.run_llm(user_input)

def main():
    @click.command()
    @click.option('--always-grant-permission', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
    @click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
    def cli(always_grant_permission, directory='.'):
        app = Main()
        app.start(always_grant_permission, directory)

    cli()

if __name__ == "__main__":
    main()
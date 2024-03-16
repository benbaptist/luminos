import click
from luminos.core import Core
import os
from prompt_toolkit import prompt
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import accept_line

bindings = KeyBindings()

# Correct Ctrl+Enter binding to submit the input
@bindings.add(Keys.ControlJ)  # ControlJ represents Ctrl+Enter in prompt_toolkit
def submit_input(event):
    accept_line(event)


is_multiline = True  # Enabling multiline input

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
                user_input = prompt("<user> ", multiline=is_multiline, key_bindings=bindings)
                # Process user_input here
                print(f"You entered: {user_input}")
            except EOFError:
                print("Exiting...")
                break
            except KeyboardInterrupt:
                print("Exiting...")
                break

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
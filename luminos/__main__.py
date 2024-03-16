import click
from luminos.core import Core
import os
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

bindings = KeyBindings()

style = Style.from_dict({
    'prompt': 'ansicyan bold',
    'warning': 'ansiwhite on_ansi_red',
})

class Main:
    def __init__(self):
        self.core = Core()

    def start(self, always_grant_permission, directory):
        # Apply the always grant permission setup
        if always_grant_permission:
            warning_message = FormattedText([
                ('class:warning', 'WARNING: You have enabled "always grant permission" mode. This provides the LLM with unprompted privileged access, which can pose potential security risks. To proceed, type "YES": '),
            ])
            print_formatted_text(warning_message)
            user_response = prompt('>')
            if user_response != 'YES':
                print('Operation cancelled. Exiting...')
                return
            os.environ['ALWAYS_GRANT_PERMISSION'] = '1'
        else:
            os.environ['ALWAYS_GRANT_PERMISSION'] = '0'

        # Change to the specified directory if provided
        if directory:
            os.chdir(directory)

        while True:
            try:
                cwd = os.getcwd()
                if len(cwd) > 20:
                    display_cwd = '...' + cwd[-17:]
                else:
                    display_cwd = cwd
                user_input = prompt(f"[user@luminos {display_cwd}]$ ", style=style, key_bindings=bindings)
                
                self.core.run_llm(user_input)
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
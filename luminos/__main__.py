from luminos.logic import Logic
from luminos.input import get_user_input, style_normal, style_warning

import click
import os
import signal
import readline
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'response': 'ansiwhite', # White text for response
    'model': 'ansigreen', # Green text for model name
})

class Main:
    def __init__(self):
        self.logic = Logic()
        self.exit_signal_count = 0
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigint(self, signum, frame):
        if self.exit_signal_count == 0:
            self.exit_signal_count += 1
            print('\nPress Ctrl+C again to exit...')
        else:
            print('\nExiting...')
            exit()

    def start(self, permissive, directory):
        # Apply the permissive setup
        if permissive:
            warning_message = FormattedText([
                ('class:warning', 'WARNING: You have enabled \"permissive\" mode. This provides the LLM with unprompted privileged access, which can pose potential security risks. To proceed, type \"YES\": '),
            ])
            print_formatted_text(warning_message, style=style_warning)
            user_response = prompt('>', style=style_warning)
            if user_response != 'YES':
                print('Operation cancelled. Exiting...')
                return
            os.environ['ALWAYS_GRANT_PERMISSION'] = '1'

            current_style = style_warning
        else:
            os.environ['ALWAYS_GRANT_PERMISSION'] = '0'

            current_style = style_normal

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
                    
                user_input = get_user_input(style=current_style, display_cwd=display_cwd)
                response = self.logic.generate_response(user_input)
                formatted_response = FormattedText([
                    ('class:response', response['message'] + '\n'),
                    ('class:model', 'Model: ' + response['model'])
                ])
                print_formatted_text(formatted_response, style=style)
            except EOFError:
                print("\nExiting...")
                break
            except KeyboardInterrupt:
                continue

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
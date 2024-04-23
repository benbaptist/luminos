import readline
import os
import signal
from getpass import getuser
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style 
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText

from luminos.logic import Logic
from luminos.exceptions import *
from luminos.commands import Commands

class Input:
    def __init__(self, permissive, directory, logic):
        self.permissive = permissive
        self.directory = directory
        self.logic = logic
        self.commands = Commands(self, logic)

        self.bindings = KeyBindings()
        readline.parse_and_bind('tab: complete')

        self.style_normal = Style.from_dict({
            'prompt': 'ansicyan bold',
        })

        self.style_warning = Style.from_dict({
            'prompt': 'ansiwhite bold ansired',
            'warning': 'bg:ansired ansiwhite bold',
        })

        self.style_response = Style.from_dict({
            'response': 'ansiwhite',
            'model': 'ansigreen',
        })

        self.style_error = Style.from_dict({
            'error': 'bg:ansired ansiwhite bold',
        })

        self.exit_signal_count = 0

    def handle_sigint(self, signum, frame):
        if self.exit_signal_count == 0:
            self.exit_signal_count += 1
            print('\nPress Ctrl+C again to exit...') 
        else:
            print('\nExiting...')
            exit()

    def get_user_input(self, style, display_cwd):
        user_input = ''

        while not user_input.strip():
            user_input = prompt(f"[{self.logic.model.model}@{self.logic.model.provider} {display_cwd}]$ ", style=style, key_bindings=self.bindings)

        return user_input

    def start(self):
        signal.signal(signal.SIGINT, self.handle_sigint)

        if self.permissive:
            warning_message = FormattedText([
                ('class:warning', 'WARNING: You have enabled "permissive" mode. This provides the LLM with unprompted privileged access, which can pose potential security risks. To proceed, type "YES": '),
            ])
            print_formatted_text(warning_message, style=self.style_warning)
            user_response = prompt('>', style=self.style_warning)

            if user_response != 'YES':
                print('Operation cancelled. Exiting...')
                return

            os.environ['ALWAYS_GRANT_PERMISSION'] = '1'  
            current_style = self.style_warning
        else:
            os.environ['ALWAYS_GRANT_PERMISSION'] = '0'
            current_style = self.style_normal

        if self.directory:
            os.chdir(self.directory)

        while True:
            try:
                cwd = os.getcwd()
                display_cwd = '...' + cwd[-17:] if len(cwd) > 20 else cwd

                user_input = self.get_user_input(current_style, display_cwd)

                if user_input.startswith('/'):
                    try:
                        response = self.commands.execute(user_input)
                        print(response)
                    except Exception as e:
                        error_message = FormattedText([
                            ('class:error', f'Error: {e}'),
                        ])
                        print_formatted_text(error_message, style=self.style_error)
                else:
                    try:
                        response = self.logic.generate_response(user_input)
                    except ModelReturnError as e:
                        error_message = FormattedText([
                            ('class:error', f'Error: {e}'),
                        ])
                        print_formatted_text(error_message, style=self.style_error)
                        continue

                    if not response:
                        print("No response generated. This is likely a Luminos error.")
                        continue

                    print(response.content)
            except EOFError:
                print("\\nExiting...")
                break
            except KeyboardInterrupt:
                continue
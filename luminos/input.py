"""Module for handling user input/output for Luminos"""

import os
import signal
import readline
from getpass import getuser
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

from luminos.logic import Logic
from luminos.exceptions import ModelReturnError

class Input:
    """Class for handling Luminos user input/output"""

    def __init__(self, logic: Logic, permissive: bool = False, directory: str = None):
        self.logic = logic
        self.permissive = permissive
        self.exit_signal_count = 0
        self.cwd = os.getcwd() if not directory else directory

        self.styles = {
            'normal': Style.from_dict({
                'prompt': 'ansicyan bold',
            }),
            'warning': Style.from_dict({
                'prompt': 'ansiwhite bold ansired',
                'warning': 'bg:#ff0000 #ffffff bold',
            }),
            'response': Style.from_dict({
                'response': 'ansiwhite',
                'model': 'ansigreen',
            }),
            'error': Style.from_dict({
                'error': 'bg:#ff0000 #ffffff bold',
            }),
        }

        self.key_bindings = KeyBindings()
        readline.parse_and_bind('tab: complete')
        signal.signal(signal.SIGINT, self.handle_sigint)

        if permissive:
            self.enable_permissive_mode()
        else:
            os.environ['ALWAYS_GRANT_PERMISSION'] = '0'

        self.session = self.create_prompt_session()

    def enable_permissive_mode(self):
        """Prompt for permissive mode and enable if confirmed"""
        confirm = self.session.prompt(
            HTML('<ansiwhite bold bg:#ff0000>WARNING: You have enabled '
                 '"permissive" mode. This provides the LLM with unprompted '
                 'privileged access, which can pose potential security risks. '
                 'To proceed, type "YES": </ansiwhite>'),
            style=self.styles['warning']
        )
        if confirm == 'YES':
            os.environ['ALWAYS_GRANT_PERMISSION'] = '1'
        else:
            print('Operation cancelled. Exiting...')
            exit()

    def create_prompt_session(self):
        """Create prompt session with current state"""
        user_input = prompt(f"[{logic.model.model}@{logic.model.provider} {display_cwd}]$ ", style=style, key_bindings=bindings)

        return user_input

    def handle_sigint(self, signum, frame):
        """Handle Ctrl+C interrupt signal"""
        if self.exit_signal_count == 0:
            self.exit_signal_count += 1
            print('\\nPress Ctrl+C again to exit...')
        else:
            print('\\nExiting...')
            exit()

    def start(self):
        """Start the Luminos input/output loop"""
        while True:
            try:
                user_input = self.session.prompt()

                if user_input.lower() == 'exit':
                    print('Exiting...')
                    break

                try:
                    response = self.logic.generate_response(user_input)
                except ModelReturnError as e:
                    error = HTML(f'<ansiwhite bg:#ff0000>Error: {e}</ansiwhite>')
                    print(error)
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

if __name__ == "__main__":
    logic = Logic()
    userio = UserIO(logic)
    userio.start()
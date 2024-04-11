from luminos.logic import Logic
from luminos.exceptions import *

import readline
import os
import signal
from getpass import getuser
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText

bindings = KeyBindings()

style_normal = Style.from_dict({
    'prompt': 'ansicyan bold',
})

style_warning = Style.from_dict({
    'prompt': 'ansiwhite bold ansired',
    'warning': 'bg:ansired ansiwhite bold',
})

style_response = Style.from_dict({
    'response': 'ansiwhite',
    'model': 'ansigreen',
})

readline.parse_and_bind('tab: complete')


# Handle user input and interactions

def get_user_input(style, display_cwd):
    user_input = ''
    while not user_input.strip():
        user_input = prompt(f"[{getuser()}@luminos {display_cwd}]$ ", style=style, key_bindings=bindings)
    return user_input


def start_user_interaction(permissive, directory, logic):
    exit_signal_count = 0

    def handle_sigint(signum, frame):
        nonlocal exit_signal_count
        if exit_signal_count == 0:
            exit_signal_count += 1
            print('\nPress Ctrl+C again to exit...')
        else:
            print('\nExiting...')
            exit()

    signal.signal(signal.SIGINT, handle_sigint)

    if permissive:
        warning_message = FormattedText([
            ('class:warning', 'WARNING: You have enabled "permissive" mode. This provides the LLM with unprompted privileged access, which can pose potential security risks. To proceed, type "YES": '),
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

    if directory:
        os.chdir(directory)

    while True:
        try:
            cwd = os.getcwd()
            display_cwd = '...' + cwd[-17:] if len(cwd) > 20 else cwd

            user_input = get_user_input(current_style, display_cwd)

            try: 
                response = logic.generate_response(user_input)
            except ModelReturnError:
                print("Failed to retrieve a response from the model. Please try again later.")
                
                continue

            if not response:
                print("No response generated. This is likely a Luminos error.")
                continue

            formatted_response = FormattedText([
                ('class:response', f'[{response.model}@luminos]# {response.content}\n'),
            ])

            print_formatted_text(formatted_response, style=style_response)
        except EOFError:
            print("\nExiting...")
            break
        except KeyboardInterrupt:
            continue
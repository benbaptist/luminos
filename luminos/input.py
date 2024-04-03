from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText

import readline
import os
import rlcompleter
import atexit
import signal
from luminos.logic import Logic

bindings = KeyBindings()

style_normal = Style.from_dict({
    'prompt': 'ansicyan bold',
})

style_warning = Style.from_dict({
    'prompt': 'ansired bold',
    'warning': 'bg:ansired ansiwhite bold',
})

style_response = Style.from_dict({
    'response': 'ansiwhite',
    'model': 'ansigreen',
})

readline.parse_and_bind('tab: complete')
histfile = os.path.expanduser("~/.luminos_history")
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, histfile)

@bindings.add("\x01")
def history_previous(event):
    readline.write_history_file(histfile)
    readline.read_history_file(histfile)
    result = readline.get_current_history_length()
    try:
        readline.replace_history_item(result - 1, readline.get_history_item(result - 1))
    except: pass

@bindings.add("\x02")
def history_next(event):
    readline.write_history_file(histfile)
    readline.read_history_file(histfile)
    result = readline.get_current_history_length()
    if result < readline.get_current_history_length():
        try:
            readline.replace_history_item(result - 1, readline.get_history_item(result - 1))
        except: pass

def get_user_input(style, display_cwd):
    user_input = ''
    while not user_input.strip():
        user_input = prompt(f"[user@luminos {display_cwd}]$ ", style=style, key_bindings=bindings)
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
                
            user_input = get_user_input(current_style, display_cwd)
            response = logic.generate_response(user_input)
            formatted_response = FormattedText([
                ('class:response', response['message'] + '\n'),
                ('class:model', 'Model: ' + response['model'])
            ])
            print_formatted_text(formatted_response, style=style_response)
        except EOFError:
            print("\nExiting...")
            break
        except KeyboardInterrupt:
            continue

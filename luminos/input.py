from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText

import readline
import os
import rlcompleter
import atexit

bindings = KeyBindings()

style_normal = Style.from_dict({
    'prompt': 'ansicyan bold',
})

style_warning = Style.from_dict({
    'prompt': 'ansired bold',
    'warning': 'bg:ansired ansiwhite bold',
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

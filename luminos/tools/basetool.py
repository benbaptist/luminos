from docstring_parser import parse
import os
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

# Define custom styles for the permission request
style = Style.from_dict({
    'permission': 'bg:ansiyellow ansiwhite bold',
    'action': 'bg:ansiblue ansiwhite bold',
    'normal': '' # Default text style
})

class BaseTool:
    name = "basetool"

    @property
    def __func__(self):
        """Converts the BaseTool system to the OpenAI-friendly 'functions' methodology."""
        func = []

        for attr in dir(self):
            if attr.startswith("__"):
                continue

            method = getattr(self, attr)

            if not callable(method) or not method.__doc__:
                continue

            docstring = parse(method.__doc__)

            if not docstring.short_description.startswith("openai.function: "):
                continue

            properties = {}

            for param in docstring.params:
                if param.type_name == "int":
                    type_name = "number"
                elif param.type_name == "str":
                    type_name = "string"
                elif param.type_name == "bool":
                    type_name = "boolean"
                elif param.type_name == "list":
                    type_name = "array"

                properties[param.arg_name] = {
                    "type": type_name,
                    "description": param.description
                }

                if type_name == "array":
                    properties[param.arg_name]["items"] = {
                        "type": "string"
                    }

            try:
                required = docstring.long_description.split(",")
            except AttributeError:
                required = []

            function = {
                "name": f"{self.name}_{attr}",
                "description": docstring.short_description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }

            func.append({
                "type": "function",
                "function": function
            })

        return func

    def safe(self, reason):
        if os.getenv('ALWAYS_GRANT_PERMISSION', '0') == '1':
            return
        permission_request = FormattedText([
            ('class:permission', '\n[Permission Request] Permission to perform the following action is requested:\n'),
            ('class:action', f'Action: {reason}\n'),
            ('class:normal', 'Grant permission? [Y/n]: ')
        ])
        print_formatted_text(permission_request, style=style)
        user_input = input().strip().upper()
        if user_input == "Y":
            return 
        else:
            raise PermissionError("Permission denied by the user.")
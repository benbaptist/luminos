from docstring_parser import parse

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
        if input(f"Permission to `{reason}` requested. Grant permission? [Y/n]: ").upper() == "Y":
            return 
        else:
            raise PermissionError("The user did not grant you permission to this action. Sorry!")
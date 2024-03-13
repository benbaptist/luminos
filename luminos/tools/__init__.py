from luminos.tools.fileio import FileIO
from luminos.tools.http import HTTP
from luminos.tools.shell import Shell

class Tools:
    def __init__(self):
        self.tools = [FileIO, HTTP, Shell]

    def call(self, name, kwargs):
        tool_name, function_name = name.split("_")

        for tool in self.tools:
            if tool.name == tool_name and hasattr(tool, function_name):
                # Create tool context
                tool_cxt = tool()

                # Call the function and return the result
                try:
                    return getattr(tool_cxt, function_name)(**kwargs)
                except Exception as e:
                    print(f"func returned error: {e}")
                    # Log and return error message to the LLM
                    return f"Tool call failed with the following error: {e}"

        raise EOFError(f"Couldn't find the method {name}")
    
    @property
    def __obj__(self):
        l = []
        for tool in self.tools:
            tool = tool()
            l += tool.__func__

        return l

    @property
    def list_methods(self):
        methods = []

        for Tool in self.tools:
            for attr in dir(Tool):
                val = getattr(Tool, attr)

                if not callable(val):
                    continue

                if not val.__doc__:
                    continue

                if not val.__doc__.startswith("openai.function: "):
                    continue

                methods.append((Tool, val))

        return methods
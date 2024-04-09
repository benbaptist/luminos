from luminos.tools import Tools
from luminos.config import Config
from luminos.system_prompt import SYSTEM_PROMPT

from luminos.models.base_model import BaseModel
from luminos.models.openai.gpt35 import GPT35

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.assistant import Assistant
from luminos.messages.tool_call import ToolCall
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

import json
import os
import time

from getpass import getuser

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'gpt': 'ansiwhite bg:ansiblack', # Grey text for GPT prompt
})

class Logic:
    def __init__(self, app):
        self.app = app
        self.model = GPT35(api_key=self.app.config.settings["OPENAI_API_KEY"])
        self.tools = Tools()

    def generate_response(self, txt):
        self.model.messages.append(User(txt))

        while True:
            self.model.system_prompt = SYSTEM_PROMPT.format(
                time=time.strftime("%Y-%m-%d %H:%M:%S"),
                current_directory=os.getcwd(),
                listing=str(os.listdir(".")),
                username=getuser()
            )

            response = self.model.generate_response()

            # TODO: if finish_reason == "tool_calls":
            # else: return {'message': message, 'model': self.model}

            if response:
                content = response['message']
                model = response['model']

                self.model.messages.append(Assistant(txt))

                tool_calls = response.get('tool_calls', [])

                for tool_call in tool_calls:
                    call_id = tool_call.id
                    tool_type = tool_call.type

                    if tool_type == "function":
                        func = tool_call.function
                        func_name = func.name
                        func_kwargs = json.loads(func.arguments)

                        tool_return = self.tools.call(func_name, call_id, func_kwargs)

                        self.model.messages.append(tool_return)
                    else:
                        raise Exception(f"Invalid tool_type {tool_type}")

                return True

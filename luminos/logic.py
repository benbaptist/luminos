from luminos.tools import Tools
from luminos.config import Config
from luminos.system_prompt import SYSTEM_PROMPT

from luminos.models.base_model import BaseModel
from luminos.models.openai.gpt35 import GPT35
from luminos.models.anthropic import BaseAnthropic

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

import json
import os
import time

from getpass import getuser

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

class Logic:
    def __init__(self, app):
        self.app = app
        self.model = BaseAnthropic(None, model="claude-3-sonnet-20240229")
        # self.model = GPT35(api_key=self.app.config.settings["OPENAI_API_KEY"])
        self.model.tools = Tools(self.model.ToolReturn)

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

            print(response.finish_reason)

            if response.finish_reason == "tool_calls":
                tool_calls = response.tool_calls
 
                for tool_call in tool_calls:
                    call_id = tool_call.id
                    tool_type = tool_call.type
 
                    if tool_type == "function":
                        func = tool_call.content
                        func_name = func.name
                        func_kwargs = json.loads(func.arguments)

                        tool_return = self.model.tools.call(func_name, call_id, func_kwargs)

                        self.model.messages.append(tool_return)
                    else:
                        raise Exception(f"Invalid tool_type {tool_type}")

            else:
                return response

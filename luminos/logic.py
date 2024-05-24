from luminos.logger import logger

from luminos.tools import Tools

from luminos.models.base_model import BaseModel
from luminos.models.openai.gpt35 import GPT35
from luminos.models.anthropic import BaseAnthropic

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

from luminos.exceptions import *

import json
import os
import time

from getpass import getuser

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

class Logic:
    def __init__(self, app, model):
        self.app = app
        self.model = model
        self.model.tools = Tools(self.model.ToolReturn)

    def generate_response(self, txt):
        self.model.add_message(User(txt))

        while True:
            self.model.system_prompt = self.model.system_prompt_template.format(
                time=time.strftime("%Y-%m-%d %H:%M:%S"),
                current_directory=os.getcwd(),
                listing=str(os.listdir(".")),
                username=getuser()
            )

            response = self.model.generate_response()

            if response.finish_reason == "tool_calls":
                logger.debug("finish_reason == tool_calls")

                if response.content:
                    print(response.content)
                
                tool_calls = response.tool_calls
 
                for tool_call in tool_calls:
                    call_id = tool_call.id
                    tool_type = tool_call.type

                    logger.debug(f"<call_id={call_id}, tool_type={tool_type}>")
 
                    if tool_type == "function":
                        func = tool_call.content
                        func_name = func.name
                        func_kwargs = json.loads(func.arguments)

                        logger.debug(f"<func={func}, func_name={func_name}, func_kwargs={func_kwargs}>")

                        tool_return = self.model.tools.call(
                            name=func_name,
                            call_id=call_id,
                            app=self.app,
                            kwargs=func_kwargs
                        )

                        self.model.add_message(tool_return)
                    else:
                        raise Exception(f"Invalid tool_type {tool_type}")

            else:
                return response

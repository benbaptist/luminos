from luminos.tools import Tools
from luminos.config import Config
from luminos.system_prompt import SYSTEM_PROMPT

from openai import OpenAI

import json
import os
import time
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'gpt': 'ansiwhite bg:ansiblack', # Grey text for GPT prompt
})

class Core:
    def __init__(self):
        self.messages = []

        # Load settings from YAML configuration
        config = Config().settings
        api_key = config.get('OPENAI_API_KEY', '')
        
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()
        
        self.tools = Tools()

    def run_llm(self, txt):
        self.messages.append(
            {
                "role": "user",
                "content": txt
            }
        )

        while True:
            # Run the LLM
            prompt = SYSTEM_PROMPT.format(
                time=time.strftime("%Y-%m-%d %H:%M:%S"),
                current_directory=os.getcwd(),
                listing=str(os.listdir("."))
            )

            _messages = [
                {
                    "role": "system",
                    "content": prompt
                }
            ] + self.messages

            response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=_messages,
                tools=self.tools.__obj__,
                tool_choice="auto",
            )

            # Extract the response message and tool calls
            choice = response.choices[0]
            
            message = choice.message.content
            finish_reason = choice.finish_reason

            self.messages.append(choice.message)

            if finish_reason == "tool_calls":
                tool_calls = choice.message.tool_calls

                for tool_call in tool_calls:
                    call_id = tool_call.id
                    tool_type = tool_call.type

                    if tool_type == "function":
                        func = tool_call.function

                        func_name = func.name
                        func_kwargs = json.loads(func.arguments)

                        func_response = self.tools.call(func_name, func_kwargs)

                        self.messages.append(
                            {
                                "tool_call_id": call_id,
                                "role": "tool",
                                "name": func_name,
                                "content": json.dumps(func_response),
                            }
                        )
                    else:
                        raise Exception(f"Invalid tool_type {tool_type}")
            else:
                cwd = os.getcwd()
                if len(cwd) > 20:
                    display_cwd = '...' + cwd[-17:]
                else:
                    display_cwd = cwd
                formatted_message = FormattedText([
                    ('class:gpt', f"[gpt@luminos {display_cwd}]# {message}")
                ])
                print_formatted_text(formatted_message, style=style)

            # Check if the finish code has been set
            if finish_reason == "stop":
                return
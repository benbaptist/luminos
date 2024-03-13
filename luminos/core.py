from luminos.tools import Tools
from luminos.system_prompt import SYSTEM_PROMPT
# from luminos.config import Config

import openai
import json

class Core:
    def __init__(self):
        self.messages = [{
            "role": "system",
            "content": SYSTEM_PROMPT
        }]
        
        self.client = openai.OpenAI()
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
            response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=self.messages,
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

                        print(f"{func_name}({func_kwargs})")
                        
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
                print(f"<gpt> {message}")

            # Check if the finish code has been set
            if finish_reason == "stop":
                return
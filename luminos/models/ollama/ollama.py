from luminos.models.base_model import BaseModel
from luminos.logger import logger
from luminos.exceptions import ModelReturnError

from luminos.messages.assistant import Assistant
from luminos.messages.tool_call import ToolCall
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

from .system_prompt import SYSTEM_PROMPT

from litellm import completion

import json

class Ollama(BaseModel):
    provider = "ollama"
    model = None

    has_tools = True
    has_vision = True

    api_base="http://localhost:11434"

    system_prompt_template = SYSTEM_PROMPT

    def __init__(self):
        super().__init__()

    def generate_response(self, stream=False):
        serialized_messages = [message.serialize() for message in self.messages]

        try:
            response = completion(
                model=f"ollama/{self.model}",
                messages=serialized_messages,
                api_base=self.api_base,
                tools=self.tools.__obj__,
                stream=stream
            )

            if stream:
                content = ""
                choice = {}

                print(f"<{self.model}> ", end="")

                for chunk in response:
                    _choice = chunk['choices'][0]
                    delta = _choice['delta']

                    print(delta.content, end="", flush=True)
                    
                    if delta.content != None:
                        content += delta.content
                    
                    for key in _choice:
                        if type(key) != str:
                            continue

                        choice[key] = _choice[key]
                    
                print()
            else:
                choice = response["choices"][0]
                print(choice)
                content = choice.message.content

                print(f"<{self.model}> {content}")
                
        except Exception as e:
            logger.error(f"Error while making request to Ollama: {e}")
            raise ModelReturnError(f"Error making request to Ollama: {e}")
        
        # finish_reason = choice["finish_reason"]

        # Parse tool calls from the response
        # try:
        #     tool_calls = tool_parser(content)
        # except Exception as e:
        #     logger.error(f"Error while parsing for potential tool calls {e}")
        #     logger.debug(content)
        #     raise ModelReturnError(f"Error while parsing for potential tool calls: {e}")

        if "tool_calls" in choice:
            print(choice["tool_calls"])

        tool_calls = []

        if len(tool_calls) > 0:
            tool_calls_data = response.choices[0].message.tool_calls

            tool_calls = [
                ToolCall(content=data.function, id=data.id, type=data.type) for data in tool_calls_data
            ]

            msg = Assistant(content)
            msg.tool_calls = tool_calls

            self.add_message(msg)
        else:
            self.add_message(Assistant(content))
            
        return Response(content=content, model=self.model, tool_calls=tool_calls)

from luminos.models.base_model import BaseModel
from luminos.logger import logger
from luminos.exceptions import ModelReturnError

from luminos.messages.assistant import Assistant
from luminos.messages.tool_call import ToolCall
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

from litellm import completion

class Ollama(BaseModel):
    provider = "ollama"
    model = "llama3:8b"

    has_tools = True
    has_vision = True

    api_base="http://localhost:11434"

    def __init__(self):
        super().__init__()

    def generate_response(self):
        # Limit to the most basic tools, for now
        self.tools.tools = ("Shell", "FileIO")

        serialized_messages = [message.serialize() for message in self.messages]

        try:
            response = completion(
                model=f"ollama_chat/{self.model}",
                messages=serialized_messages,
                api_base=self.api_base,
                # tools=self.tools.__obj__,
                # tool_choice="auto",
            )

            logger.debug(response)
        except Exception as e:
            logger.error(f"Error while making request to Ollama: {e}")
            raise ModelReturnError(f"Error making request to Ollama: {e}")
        
        choice = response.choices[0]
        
        content = choice.message["content"]
        finish_reason = choice.finish_reason

        # Parse tool calls from the response
        tool_calls = []

        if finish_reason == "tool_calls":
            tool_calls_data = response.choices[0].message.tool_calls

            tool_calls = [
                ToolCall(content=data.function, id=data.id, type=data.type) for data in tool_calls_data
            ]

            msg = Assistant(content)
            msg.tool_calls = tool_calls

            self.add_message(msg)
        else:
            self.add_message(Assistant(content))
            
        return Response(content=content, model=self.model, tool_calls=tool_calls, finish_reason=finish_reason)

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.tool_call import ToolCall

from luminos.types.function import Function

from luminos.models.base_model import BaseModel

from .messages.tool_return import ToolReturn
from .messages.assistant import Assistant

from luminos.exceptions import *

from anthropic.types import (
    ContentBlock,
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    ImageBlockParam,
    Message,
    MessageDeltaEvent,
    MessageDeltaUsage,
    MessageParam,
    MessageStartEvent,
    MessageStopEvent,
    MessageStreamEvent,
    TextBlock,
    TextBlockParam,
    TextDelta,
)

from anthropic.types.beta.tools import (
    ToolUseBlock
)

import anthropic

class BaseAnthropic(BaseModel):
    ToolReturn = ToolReturn
    Assistant = Assistant

    def __init__(self, api_key: str, model: str):
        super().__init__()
        
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic() # api_key=self.api_key

    @property
    def _tools(self):
        tools = []

        for tool in self.tools.__obj__:
            function = tool["function"]

            tools.append({
                "name": function["name"],
                "description": function["description"],
                "input_schema": function["parameters"]
            })

        return tools

    def generate_response(self):
        serialized_messages = [msg.serialize() for msg in self.messages]

        try:
            response = self.client.beta.tools.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=serialized_messages,
                system=self.system_prompt,
                tools=self._tools
            )
        except anthropic.RateLimitError as e:
            raise ModelReturnError(f"RateLimitError: {e}")
        except anthropic.BadRequestError as e:
            print(e)

            raise ModelReturnError(f"BadRequestError: {e}")

        tool_calls = []

        asst = self.Assistant("")
        asst.model = self.model
        
        self.messages.append(asst)

        for block in response.content:
            if type(block) == ToolUseBlock:
                func = Function(
                    name=block.name,
                    arguments=block.input
                )
                
                tool_call = ToolCall(
                    content=func,
                    type="function",
                    id=block.id
                )

                asst.tool_calls.append(tool_call)

                content = ""
            elif type(block) == TextBlock:
                asst.content = response.content[0].text
        
        return asst
from luminos.logger import logger
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

    provider="anthropic"
    model = "claude-3-sonnet-20240229"

    has_tools = True
    has_vision = True

    api_key = None
    temperature = 0.5
    max_tokens = 4096

    def __init__(self):
        super().__init__()

        self.client = None

    @property
    def messages(self):
        # Override the injection of a System prompt here; 
        # it's passed as an argument to .create() and not needed
        return self._messages

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
        if not self.client:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        serialized_messages = [msg.serialize() for msg in self.messages]

        asst = self.Assistant("")
        asst.model = self.model

        try:
            response = self.client.beta.tools.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=serialized_messages,
                system=self.system_prompt,
                tools=self._tools,
                temperature=self.temperature
            )

            logger.debug(response)
        except anthropic.RateLimitError as e:
            raise ModelReturnError(f"RateLimitError: {e}")
        except anthropic.BadRequestError as e:

            logger.error("**DEBUGGING***")
            logger.error("*" * 16)
            logger.error(self.messages)
            logger.error("*" * 4)

            for msg in self.messages:
                logger.error(f"--- {msg.serialize()}")
                
            logger.error("*" * 16)
            
            raise ModelReturnError(f"BadRequestError: {e}")
        
        # logger.debug("Appending assistant object to messages")
        self.add_message(asst)

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
                if not asst.content:
                    asst.content = ""
                    
                asst.content += response.content[0].text

        # if len(asst.content) < 1:
        #     try:
        #         logger.debug("Removing stale assistant object from messages")
        #         self.messages.remove(asst)
        #     except:
        #         pass
        
        return asst

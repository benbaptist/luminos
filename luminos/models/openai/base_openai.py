from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.assistant import Assistant
from luminos.messages.tool_call import ToolCall
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

from ..base_model import BaseModel

from openai import OpenAI
from typing import List

import json

class BaseOpenAI(BaseModel):
    def __init__(self, api_key: str, model: str):
        super().__init__()

        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def __str__(self):
        return self.model

    def generate_response(self) -> Response:
        serialized_messages = [message.serialize() for message in self.messages]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=serialized_messages,
            tools=self.tools.__obj__,
            tool_choice="auto",
        )
        
        choice = response.choices[0]
        
        content = choice.message.content
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

            self.messages.append(msg)
        else:
            self.messages.append(Assistant(content))
            
        return Response(content=content, model=self.model, tool_calls=tool_calls, finish_reason=finish_reason)

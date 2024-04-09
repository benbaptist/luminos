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

class BaseOpenAI(BaseModel):
    def __init__(self, api_key: str, model: str):
        super().__init__()

        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self) -> Response:
        serialized_messages = [message.serialize() for message in messages]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=serialized_messages,
            tools={},
            tool_choice="auto",
        )
        content = response.choices[0].message.content

        # Parse tool calls from the response
        tool_calls_data = response.choices[0].message.get('tool_calls', [])
        tool_calls = [ToolCall(content=data['content'], tool_call_id=data['id'], name=data['name'], arguments=data['arguments']) for data in tool_calls_data]
        
        return Response(content=content, model=self.model, tool_calls=tool_calls)

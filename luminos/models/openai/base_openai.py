from luminos.messages import BaseMessage, System, User, Assistant, ToolReturn, Response, ToolCall
from openai import OpenAI
from typing import List

class BaseOpenAI:
    def __init__(self, api_key: str, model: str):
        super().__init__()

        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, messages: List[BaseMessage]) -> Response:
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

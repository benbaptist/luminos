from luminos.messages.base_message import BaseMessage

import json

class ToolReturn(BaseMessage):
    def __init__(self, content: str, call_id: str, name: str):

        super().__init__(content)
        self.call_id = call_id
        self.name = name

    def serialize(self) -> dict:
        # Return OpenAI-style tool_return

        return {
            'role': 'tool',
            'content': json.dumps(self.content),
            'tool_call_id': self.call_id,
            'name': self.name
        }

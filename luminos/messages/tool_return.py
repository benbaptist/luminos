from luminos.messages.base_message import BaseMessage

import json

class ToolReturn(BaseMessage):
    def __init__(self, content: str, name: str, id: str):

        super().__init__(content)
        self.id = id
        self.name = name

    def serialize(self) -> dict:
        # Return OpenAI-style tool_return

        return {
            'role': 'tool',
            'content': json.dumps(self.content),
            'tool_call_id': self.id,
            'name': self.name
        }

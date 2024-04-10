from luminos.messages.tool_return import ToolReturn

import json

class ToolReturn(ToolReturn):
    def __init__(self, content: str, name: str, id: str):

        super().__init__(content, name, id)

    def serialize(self) -> dict:
        # Return Anthropic-style tool_result

        return {
            'role': 'user',
            'content': [
                {
                    'type': "tool_result",
                    'tool_use_id': self.id,
                    "content": json.dumps(self.content)
                }
            ]
        }
from luminos.messages.base_message import BaseMessage

class ToolReturn(BaseMessage):
    def __init__(self, content: str, tool_call_id: str, name: str):
        super().__init__(content)
        self.tool_call_id = tool_call_id
        self.name = name

    def serialize(self) -> dict:
        return {
            'role': 'tool_return',
            'content': self.content,
            'tool_call_id': self.tool_call_id,
            'name': self.name
        }

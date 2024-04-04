from luminos.messages.base_message import BaseMessage

class ToolCall(BaseMessage):
    def __init__(self, content: str, tool_call_id: str, name: str, arguments: dict):
        super().__init__(content)
        self.tool_call_id = tool_call_id
        self.name = name
        self.arguments = arguments

    def serialize(self) -> dict:
        # Return OpenAI-style tool_call

        return {
            'role': 'tool_call',
            'content': self.content,
            'tool_call_id': self.tool_call_id,
            'name': self.name,
            'arguments': self.arguments
        }

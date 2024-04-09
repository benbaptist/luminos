from luminos.messages.base_message import BaseMessage

class ToolCall(BaseMessage):
    def __init__(self, content: str, type: str, id: str):
        super().__init__(None)
        self.content = content
        self.type = type
        self.id = id

    # I don't know what I was doing here.
    # @property
    # def name(self):
    #     return self.content.name

    # @property
    # def arguments(self):
    #     return self.content.arguments

    def serialize(self) -> dict:
        # Return OpenAI-style tool_call

        return {
            'type': self.type,
            'id': self.id,
            'function': {
                "name": self.content.name,
                "arguments": self.content.arguments
            }
        }

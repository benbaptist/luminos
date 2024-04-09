from luminos.messages.base_message import BaseMessage

class Assistant(BaseMessage):
    def __init__(self, content: str, tool_calls=[]):
        super().__init__(content)
        self.tool_calls = tool_calls

    def serialize(self) -> dict:
        obj = {
            'role': 'assistant', 
            'content': self.content
        }

        if len(self.tool_calls) > 0:
            obj["tool_calls"] = [tool_call.serialize() for tool_call in self.tool_calls]

        return obj
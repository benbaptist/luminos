from luminos.messages.base_message import BaseMessage

class Assistant(BaseMessage):
    def serialize(self) -> dict:
        return {'role': 'assistant', 'content': self.content}

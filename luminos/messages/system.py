from luminos.messages.base_message import BaseMessage

class SystemMessage(BaseMessage):
    def serialize(self) -> dict:
        return {'role': 'system', 'content': self.content}

from luminos.messages.base_message import BaseMessage

class UserMessage(BaseMessage):
    def serialize(self) -> dict:
        return {'role': 'user', 'content': self.content}

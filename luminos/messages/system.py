from luminos.messages.base_message import BaseMessage

class SystemMessage(BaseMessage):
    def serialize(self) -> dict:
        # Return OpenAI-style system role
        
        return {'role': 'system', 'content': self.content}

from abc import ABC, abstractmethod
from typing import List, Dict

class BaseModel(ABC):
    def __init__(self):
        self.messages = []
        self.system_prompt = ""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content
        })

    def clear_messages(self):
        self.messages = []

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

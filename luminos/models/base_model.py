from abc import ABC, abstractmethod
from typing import List, Dict

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.assistant import Assistant
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

class BaseModel(ABC):
    def __init__(self):
        self.messages = []
        self.system_prompt = ""
    
    def __str__(self):
        return None

    @abstractmethod
    def generate_response(self):
        pass

    def add_message(self, role: str, content: str):
        {
            "assistant": Assistant,
            "system": System,
            "user": User
        }

        Message = _[role]
        
        self.messages.append(Message(Content))

    def clear_messages(self):
        self.messages = []

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

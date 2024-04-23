from abc import ABC, abstractmethod
from typing import List, Dict

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.assistant import Assistant
from luminos.messages.tool_call import ToolCall
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

class BaseModel(ABC):
    System = System
    User = User
    Assistant = Assistant
    ToolCall = ToolCall
    ToolReturn = ToolReturn
    Response = Response

    provider=None
    model=None

    has_vision = False
    has_tools = False

    def __init__(self):
        self._messages = []
        self.system_prompt = ""

    def __str__(self):
        return None

    @abstractmethod
    def generate_response(self):
        pass

    def add_message(self, message: BaseMessage):
        self._messages.append(message)

    @property
    def messages(self):
        # Automatically inject system prompt
        return [System(self.system_prompt)] + self._messages
    
    @messages.setter
    def messages(self, _):
        self._messages = _

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.assistant import Assistant
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

from luminos.models.base_model import BaseModel
import anthropic

class BaseAnthropic(BaseModel):
    def __init__(self, api_key: str, model: str):
        super().__init__()
        
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic() # api_key=self.api_key

    def generate_response(self) -> Response:
        serialized_messages = [msg.serialize() for msg in self.messages]

        print(serialized_messages)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=serialized_messages,
            system=self.system_prompt
        )

        content = response.content[0].text

        self.messages.append(Assistant(content))
        
        return Response(content=content, model=self.model, tool_calls=[])

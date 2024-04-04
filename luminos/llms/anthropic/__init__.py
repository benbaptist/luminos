from luminos.messages import BaseMessage, Response, ToolCall
import anthropic

class BaseAnthropic:
    # TODO: split off separate Claude models into their own classes, akin to how it's implemented for openai
    
    def __init__(self, api_key: str, model: str):
        super().__init__()
        
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_response(self, messages: list[BaseMessage]) -> Response:
        anthropic_messages = [{'role': msg.role, 'content': msg.content} for msg in messages]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=anthropic_messages,
            system=self.system_prompt
        )
        
        # Assuming 'response.content' is the desired output for simplicity. Adjust as needed for actual API structure.
        content = ''.join([block.text for block in response])
        return Response(content=content, model=self.model, tool_calls=[])

from luminos.models.base_model import BaseModel
from luminos.logger import logger
from luminos.exceptions import ModelReturnError

from litellm import completion

class Ollama(BaseModel):
    provider = "ollama"
    model = "llama3"

    has_tools = True
    has_vision = True

    api_base="http://localhost:11434"

    def __init__(self):
        super().__init__()

    def generate_response(self, messages):
        try:
            response = completion(
                model=f"ollama_chat/{self.model}",
                messages=messages,
                api_base=self.api_base
            )

            logger.debug(response)
            return response
        except Exception as e:
            logger.error(f"Error while making request to Ollama: {e}")
            raise ModelReturnError(f"Error making request to Ollama: {e}")

from luminos.models.base_model import BaseModel
from luminos.logger import logger
from luminos.exceptions import ModelReturnError

from litellm import completion

class OllamaModel(BaseModel):
    provider = "ollama"

    has_tools = True
    has_vision = True

    api_base="http://localhost:11434"

    def __init__(self, api_key: str, model: str = "ollama/llama3"):
        super().__init__()
        self.api_key = api_key
        self.model = model
        # Note: API key might not be used in this API call based on the example given

    def generate_response(self, messages):
        try:
            response = completion(
                model=self.model,
                messages=messages,
                api_base=self.api_base
            )
            logger.debug(response)
            return response
        except Exception as e:
            logger.error(f"Error while making request to Ollama: {e}")
            raise ModelReturnError(f"Error making request to Ollama: {e}")

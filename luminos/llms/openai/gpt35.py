from luminos.llms.openai_model import OpenAIModel

class GPT35(OpenAIModel):
    def __init__(self, api_key: str):
        super().__init__(api_key, model="gpt-3.5")

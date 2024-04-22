from luminos.models.openai.base_openai import BaseOpenAI

class GPT4(BaseOpenAI):
    def __init__(self, api_key: str):
        super().__init__(api_key, model="gpt-4-turbo")

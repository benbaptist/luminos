from luminos.models.openai.base_openai import BaseOpenAI

class GPT4oMini(BaseOpenAI):
    has_vision = True
    model = "gpt-4o-mini"

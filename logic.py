from luminos.tools import Tools
from luminos.config import Config
from luminos.system_prompt import SYSTEM_PROMPT

from luminos.models.base_model import BaseModel
from luminos.models.openai.gpt35 import GPT35
from luminos.models.anthropic import BaseAnthropic
# Add imports for other available model classes here

from luminos.messages.base_message import BaseMessage
from luminos.messages.system import System
from luminos.messages.user import User
from luminos.messages.tool_return import ToolReturn
from luminos.messages.response import Response

from luminos.exceptions import *

import json
import os
import time

from getpass import getuser

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

def map_model_config(provider, model_name):
    """
    Map the config provider and model name to the corresponding model class
    """
    provider_mapping = {
        "openai": GPT35,
        "anthropic": BaseAnthropic,
        # Add other providers here
    }
    
    name_mapping = {
        # Map model names to classes here
    }
    
    model_class = provider_mapping.get(provider, BaseModel)
    if model_name:
        model_class = name_mapping.get(model_name, model_class)
        
    return model_class

class Logic:
    def __init__(self, app):
        self.app = app
        config = app.config.settings["model"]
        provider = config["provider"]
        model_name = config["name"]
        
        model_class = map_model_config(provider, model_name)
        model_kwargs = {}
        if provider == "openai":
            model_kwargs["api_key"] = self.app.config.settings["api"]["openai_key"]
        elif provider == "anthropic":
            model_kwargs["model"] = model_name
            
        self.model = model_class(**model_kwargs)
        self.model.tools = Tools(self.model.ToolReturn)

    def generate_response(self, txt):
        ...
        # Existing method body
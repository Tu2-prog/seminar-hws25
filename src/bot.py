from enum import Enum
from src.model import APIClient, ModelType

class Bot:
    def __init__(self, api_type: str, model_type: ModelType):
        self.model = self.initialize_model(api_type, model_type)

    def initialize_model(self, api_type: str, model_type: ModelType):
        match model_type:
            case ModelType.LLAMA4:
                return APIClient.get_model(api_type, "meta-llama/llama-4-scout-17b-16e-instruct")
            case ModelType.DEEPSEEK:
                return APIClient.get_model(api_type, "deepseek/deepseek-3b")
            case ModelType.CHEAP:
                return APIClient.get_model(api_type, "llama-3.1-8b-instant")
            case ModelType.OPENAI:
                return APIClient.get_model(api_type, "gpt-4o-mini")
            case ModelType.NANO:
                return APIClient.get_model(api_type, "gpt-4.1-nano")
            case _:
                raise ValueError(f"Unsupported model type: {model_type}")
            
class Agent:
    def __init__(self, bot: Bot):
        self.bot = bot

    # ...existing code...
    def respond(self, prompt: str) -> str:
        response = self.bot.model.invoke([{"role": "user", "content": prompt}])
        return response.content 
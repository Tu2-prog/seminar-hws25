from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from enum import Enum
from dotenv import load_dotenv
import os

class ModelType(Enum):
    LLAMA4 = "llama4"
    DEEPSEEK = "deepseek"
    CHEAP = "cheap"
    OPENAI = "openai"
    NANO = "nano"

class APIClient:
    @staticmethod
    def get_model(api_type: str, model_name: str):
        load_dotenv()
        if api_type == "Groq":
            api_key = os.getenv("API_KEY")
            if not api_key:
                raise ValueError("API_KEY environment variable is not set.")
            return ChatGroq(
                api_key=api_key,
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0.7,
            )
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            return ChatOpenAI(
                model_name=model_name,
                temperature=0.7,
                openai_api_key=api_key,
            )
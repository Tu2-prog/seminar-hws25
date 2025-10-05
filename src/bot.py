import json
import re
from model import APIClient, ModelType


class Bot:
    def __init__(self, api_type: str, model_type: ModelType):
        self.model = self.initialize_model(api_type, model_type)

    def initialize_model(self, api_type: str, model_type: ModelType):
        match model_type:
            case m if m == ModelType.LLAMA4:
                return APIClient.get_model(
                    api_type, "meta-llama/llama-4-scout-17b-16e-instruct"
                )
            case m if m == ModelType.DEEPSEEK:
                return APIClient.get_model(api_type, "deepseek/deepseek-3b")
            case m if m == ModelType.CHEAP:
                return APIClient.get_model(api_type, "llama-3.1-8b-instant")
            case m if m == ModelType.OPENAI:
                return APIClient.get_model(api_type, "gpt-4o-mini")
            case m if m == ModelType.NANO:
                return APIClient.get_model(api_type, "gpt-4.1-nano")
            case _:
                raise ValueError(f"Unsupported model type: {model_type}")


class Agent:
    def __init__(self, bot: Bot):
        self.bot = bot

    def extract_json_from_llm_output(self, llm_output: str):
        # Find all JSON blocks in the output
        json_blocks = re.findall(
            r"```(?:json)?\s*(\{.*?\})\s*```", llm_output, re.DOTALL
        )

        if json_blocks:
            # Try each JSON block until one works
            for json_str in json_blocks:
                try:
                    json_str = self.clean_json(json_str)
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    continue
            # If none worked, try the last one with error
            json_str = self.clean_json(json_blocks[-1])
        else:
            # No code blocks, try the whole output
            json_str = self.clean_json(llm_output.strip())

        return json.loads(json_str)

    def clean_json(self, json_str):
        """Clean up common LLM JSON formatting issues."""
        # Remove literal backslash before newlines: \n\\ -> \n
        json_str = re.sub(r"\\n\\\\", r"\\n", json_str)

        # Fix invalid escapes (backslash followed by non-escape chars)
        json_str = re.sub(r'\\([^"\\/bfnrtu])', r"\\\\\1", json_str)

        return json_str.strip()

    def respond(self, prompt: str, parameters: dict = {}) -> str:
        messages = [{"role": "user", "content": prompt.format(**parameters)}]
        response = self.bot.model.invoke(messages)
        # print(response.content)
        parsed = self.extract_json_from_llm_output(response.content)
        return response.content, parsed

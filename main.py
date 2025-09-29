from src.bot import Agent, Bot
from src.model import ModelType

if __name__ == "__main__":
    bot = Agent(Bot("Groq", ModelType.OPENAI))
    response = bot.respond("What is the capital of France?")
    print(response)
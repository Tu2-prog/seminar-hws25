from src.bot import Agent, Bot
from src.model import ModelType
from src.log_manager import LogManager

log_manager = LogManager()

if __name__ == "__main__":
    bot = Agent(Bot("Groq", ModelType.OPENAI))
    response = bot.respond("What is the capital of France?")
    log_manager.log("User: What is the capital of France?")
    log_manager.log(f"Bot: {response}")
    log_manager.log_to_file(
        f"User: What is the capital of France?\nBot: {response}", "./logs/chat_log.csv"
    )

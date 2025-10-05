from bot import Bot
import json
import os
from prompts import review_prompt
from datetime import datetime


class Reviewer:
    def __init__(self, bot: Bot):
        # Always create a base logs directory in the project
        self.bot = bot
        self.base_log_dir = os.path.join(os.path.dirname(__file__), "..", "reviews")
        os.makedirs(self.base_log_dir, exist_ok=True)

    def review(self, language, documentation):
        try:
            messages = [
                {
                    "role": "user",
                    "content": review_prompt.format(
                        language=language, documentation=documentation
                    ),
                }
            ]
            response = self.bot.model.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error occurred while reviewing: {e}")

    def log_to_file(self, message, bot_type, file_path):
        date_dir = os.path.join("reviews", bot_type, os.path.dirname(file_path))
        os.makedirs(date_dir, exist_ok=True)
        full_path = os.path.join(date_dir, os.path.basename(file_path))
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(date_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        full_path = os.path.join(date_dir, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            if isinstance(message, dict):
                f.write(json.dumps(message, indent=2, ensure_ascii=False))
            else:
                f.write(str(message))

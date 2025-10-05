import json
import os
from datetime import datetime


class LogManager:
    """Central Log Manager for logging the content of the LLM agents."""

    def __init__(self):
        # Always create a base logs directory in the project
        self.base_log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(self.base_log_dir, exist_ok=True)

    def log_to_file(self, message, bot_type, file_path):
        # Create a subdirectory for each bot_type
        dir_path = os.path.join(self.base_log_dir, bot_type.lower())
        os.makedirs(dir_path, exist_ok=True)
        # Create a subdirectory for each date and store the logs there
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(dir_path, date_str)
        os.makedirs(date_dir, exist_ok=True)

        # Set the correct file extension
        if isinstance(message, dict):
            if not file_path.endswith(".json"):
                file_path += ".json"
        else:
            if not file_path.endswith(".txt"):
                file_path += ".txt"

        full_path = os.path.join(date_dir, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            if isinstance(message, dict):
                json.dump(message, f, indent=2, ensure_ascii=False)
            else:
                f.write(str(message))

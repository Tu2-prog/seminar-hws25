import os


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
        full_path = os.path.join(dir_path, file_path)
        with open(full_path, "w") as f:
            f.write(message)

import os


class LogManager:
    """Central Log Manager for logging the content of the LLM agents."""

    def __init__(self):
        # Create a directory for logs if it doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def log(self, message):
        print(message)

    def log_to_file(self, message, file_path):
        with open(file_path, "a") as file:
            file.write(message + "\n")

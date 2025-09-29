from enum import Enum

class LogManager:
    """Central Log Manager for loggin the content of the LLM agents from JSON and put it into a csv file."""
    def log(self, message):
        print(message)

    def log_to_file(self, message, file_path):
        with open(file_path, 'a') as file:
            file.write(message + '\n')
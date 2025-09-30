from langchain_core.prompts import ChatPromptTemplate

test_prompt = "What is the capital of France?"

zero_shot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an experienced software engineer "
            "that is well-versed in the art of software development, "
            "especially in writing understandable and maintable documentation for code.",
        ),
        (
            "human",
            "You are given a code snippet written in {language}. Your task is to generate clear and concise documentation for the provided code. The documentation should be easy to understand and help other developers quickly grasp the purpose and functionality of the code."
            "\n\nHere is the code snippet:\n{code_snippet}\n\nPlease provide the documentation below:",
        ),
    ]
)

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser


class DocumentationResponse(BaseModel):
    language: str
    thoughts: str
    documentation: str


class DocumentationReview(BaseModel):
    correctness: float
    completeness: float
    maintainability: float
    readability: float
    review: str


documentation_parser = PydanticOutputParser(pydantic_object=DocumentationResponse)
zero_shot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an experienced software engineer that is well-versed in the art of software development, "
            "especially in writing understandable and maintainable documentation for code. "
            "Wrap the content in a JSON object following this format:\n{format_instructions}\n\n"
            'CRITICAL: In JSON, use \\n for newlines, \\" for quotes, and \\\\ for backslashes. '
            "Do NOT use triple quotes (\"\"\" or '''). All strings must be on one line with escaped newlines.",
        ),
        (
            "human",
            "You are given a code snippet written in {language}. Your task is to generate clear and concise documentation for the provided code itself, i.e. docstrings or javadoc."
            "The documentation should be easy to understand and help other developers quickly grasp the purpose "
            "and functionality of the code."
            "\n\nHere is the code snippet:\n{code_snippet}\n\nPlease only provide the documentation below and do not repeat the code snippet:",
        ),
    ]
).partial(format_instructions=documentation_parser.get_format_instructions())

review_parser = PydanticOutputParser(pydantic_object=DocumentationReview)
review_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert software engineer. You can evaluate the quality of code documentation based on the following criteria: correctness, completeness, maintainability, and readability."
            "You rate the quality of the documentation on a scale from 0 to 5 for each criterion, where 0 is poor and 5 is excellent. At the end, you provide a clear summary why you rated the documentation that way."
            "Wrap the content in a JSON object following this format and provide no other text:\n{format_instructions}",
        ),
        (
            "human",
            "Your task is to review the following documentation of a {language} code."
            "Here is the documentation:\n{documentation}\n\nPlease provide your review below and be as fair as possible:",
        ),
    ]
).partial(format_instructions=review_parser.get_format_instructions())

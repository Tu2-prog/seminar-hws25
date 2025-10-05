from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
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


examples = [
    {
        "language": "Python",
        "code_snippet": """def add(a, b):
    return a + b""",
        "documentation": '''
    """
    Adds two numbers together.
    """
    ''',
    },
    {
        "language": "Java",
        "code_snippet": """public int add(int a, int b) {
    return a + b;
}""",
        "documentation": """/**
 * Adds two integers together.
 * @param a the first integer
 * @param b the second integer
 * @return the sum of a and b
 */""",
    },
    {
        "language": "JavaScript",
        "code_snippet": """function add(a, b) {
    return a + b;
}""",
        "documentation": """/**
 * Adds two numbers together.
 * @param a the first number
 * @param b the second number
 * @return the sum of a and b
 */""",
    },
]


documentation_parser = PydanticOutputParser(pydantic_object=DocumentationResponse)
zero_shot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an experienced software engineer that is well-versed in the art of software development, "
            "especially in writing understandable and maintainable documentation for code. "
            "Wrap the content in a JSON object following this format:\n{format_instructions}\n\n"
            "CRITICAL: Return ONLY valid JSON. The 'documentation' field must be a single-line string with escaped characters:\n"
            "- Use \\n (two characters: backslash followed by n) for line breaks\n"
            '- Use \\" (backslash followed by quote) for quotes within strings\n'
            "- Use \\\\ (two backslashes) for literal backslashes\n"
            "- Do NOT use line continuation backslashes (\\) at the end of lines\n"
            "- Do NOT use triple quotes\n"
            "- The entire documentation string must be on ONE line in the JSON\n\n"
            'Example of correct format: {{"documentation": "def example():\\n    \\"\\"\\"\\n    A function\\n    \\"\\"\\"\\n    pass"}}\n'
            "IMPORTANT: You only return the desired correct JSON object with no additional text before or after.",
        ),
        (
            "human",
            "You are given a code snippet written in {language}. Your task is to generate clear and concise documentation for the provided code itself, i.e. docstrings or javadoc. "
            "The documentation should be easy to understand and help other developers quickly grasp the purpose and functionality of the code."
            "\n\nHere is the code snippet:\n{code_snippet}\n\nPlease provide the documentation:",
        ),
    ]
).partial(format_instructions=documentation_parser.get_format_instructions())

# First, create the few-shot component (just the examples)
few_shot_examples = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=ChatPromptTemplate.from_messages(
        [
            (
                "human",
                "You are given a code snippet written in {language}.\n\nHere is the code snippet:\n{code_snippet}\n\nPlease provide the documentation:",
            ),
            ("assistant", "{documentation}"),
        ]
    ),
)

# Then, create the full prompt that includes system message, examples, and the actual query
few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an experienced software engineer that is well-versed in the art of software development, "
            "especially in writing understandable and maintainable documentation for code. "
            "Wrap the content in a JSON object following this format:\n{format_instructions}\n\n"
            "CRITICAL: Return ONLY valid JSON. The 'documentation' field must be a single-line string with escaped characters:\n"
            "- Use \\n (two characters: backslash followed by n) for line breaks\n"
            '- Use \\" (backslash followed by quote) for quotes within strings\n'
            "- Use \\\\ (two backslashes) for literal backslashes\n"
            "- Do NOT use line continuation backslashes (\\) at the end of lines\n"
            "- Do NOT use triple quotes\n"
            "- The entire documentation string must be on ONE line in the JSON\n\n"
            "IMPORTANT: You only return the desired correct JSON object with no additional text before or after.",
        ),
        few_shot_examples,
        (
            "human",
            "You are given a code snippet written in {language}. Your task is to generate clear and concise documentation for the provided code itself, i.e. docstrings or javadoc. "
            "The documentation should be easy to understand and help other developers quickly grasp the purpose "
            "and functionality of the code."
            "\n\nHere is the code snippet:\n{code_snippet}\n\nPlease provide the documentation:",
        ),
    ]
).partial(format_instructions=documentation_parser.get_format_instructions())


chain_of_thought_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an experienced software engineer that is well-versed in the art of software development, "
            "especially in writing understandable and maintainable documentation for code. "
            "Wrap the content in a JSON object following this format:\n{format_instructions}\n\n"
            "CRITICAL: Return ONLY valid JSON. The 'documentation' field must be a single-line string with escaped characters:\n"
            "- Use \\n (two characters: backslash followed by n) for line breaks\n"
            '- Use \\" (backslash followed by quote) for quotes within strings\n'
            "- Use \\\\ (two backslashes) for literal backslashes\n"
            "- Do NOT use line continuation backslashes (\\) at the end of lines\n"
            "- Do NOT use triple quotes\n"
            "- The entire documentation string must be on ONE line in the JSON\n\n"
            'Example of correct format: {{"documentation": "def example():\\n    \\"\\"\\"\\n    A function\\n    \\"\\"\\"\\n    pass"}}\n'
            "IMPORTANT: You only return the desired correct JSON object with no additional text before or after.",
        ),
        (
            "human",
            "You are given a code snippet written in {language}. Your task is to generate clear and concise documentation for the provided code itself, i.e. docstrings or javadoc. "
            "Analyze the code step-step and include those in your thoughts. Explain what parameters there are, what exceptions might be raised and what gets returned in the end."
            "After the thorough analysis, provide the appropriate code documentation in the documentation field."
            "The documentation should be easy to understand and help other developers quickly grasp the purpose and functionality of the code."
            "\n\nHere is the code snippet:\n{code_snippet}\n\nPlease provide the documentation:",
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
            "Wrap the content in a JSON object following this format and provide no other text:\n{format_instructions}"
            'CRITICAL: In JSON, use \\n for newlines, \\" for quotes, and \\\\ for backslashes. '
            "IMPORTANT: You only return the desired JSON object."
            "Do NOT use triple quotes (\"\"\" or '''). All strings must be on one line with escaped newlines.",
        ),
        (
            "human",
            "Your task is to review the following documentation of a {language} code."
            "Here is the documentation:\n{documentation}\n\nPlease provide your review below and be as fair as possible:",
        ),
    ]
).partial(format_instructions=review_parser.get_format_instructions())

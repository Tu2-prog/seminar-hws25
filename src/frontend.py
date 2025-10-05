import streamlit as st
from bot import Bot, Agent
from model import ModelType
from prompts import zero_shot_prompt
from log_manager import LogManager
from datetime import datetime
from llm_evalute import Reviewer


st.title("Welcome to the Streamlit App")
language = st.selectbox(
    "Select Programming Language:",
    ["Python", "JavaScript", "Java", "C++", "Go", "Ruby", "PHP", "Swift", "Kotlin"],
)
api_type = st.selectbox("Select API Type:", ["Groq", "OpenAI"])
bot_type = st.selectbox("Select Bot Type:", [e.name for e in ModelType])
code_input = st.text_area("Paste your code here:", height=200)

if st.button("Generate Documentation"):
    if code_input.strip() == "":
        st.warning("Please paste some code to generate documentation.")
    else:
        agent = Agent(Bot(api_type, ModelType[bot_type]))
        log_manager = LogManager()
        reviewer = Reviewer(Bot(api_type, ModelType[bot_type]))

        parameters = {"language": language, "code_snippet": code_input}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        documentation, parsed_documentation = agent.respond(
            zero_shot_prompt, parameters
        )
        review = reviewer.review(language, parsed_documentation["documentation"])

        log_manager.log_to_file(
            parsed_documentation,
            bot_type,
            f"{language}_code_documentation_log_{timestamp}",
        )
        reviewer.log_to_file(
            review, bot_type, f"{language}_code_review_log_{timestamp}.txt"
        )

        # Display the generated documentation
        st.subheader("Generated Documentation")
        st.code(parsed_documentation["documentation"], language="python")

        st.subheader("Review")
        st.text(review)

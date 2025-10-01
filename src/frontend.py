import streamlit as st
from bot import Bot, Agent
from model import ModelType
from prompts import zero_shot_prompt
from log_manager import LogManager
from datetime import datetime

st.title("Welcome to the Streamlit App")
language = st.selectbox(
    "Select Programming Language:", ["Python", "JavaScript", "Java"]
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
        parameters = {"language": language, "code_snippet": code_input}
        documentation = agent.respond(zero_shot_prompt, parameters)
        # file name needs to include timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_manager.log_to_file(
            documentation, bot_type, f"documentation_log_{timestamp}.txt"
        )

        # Display the generated documentation
        st.subheader("Generated Documentation")
        st.code(documentation, language="python")

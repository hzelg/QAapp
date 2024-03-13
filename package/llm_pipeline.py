import streamlit as st
import openai

openai.api_base = "https://hkust.azure-api.net"
openai.api_key = st.secrets["OPEN_AI_KEY"]
openai.api_type = "azure"
openai.api_version = "2023-12-01"

def process_question_insights():
    return

def display_question_insights():
    with st.container(border = True):
        st.subheader("LLM Feedback")

def submit_question(formatted_question):
    prev_prompt = ""
    with open("prompt.txt", "r") as file:
        prev_prompt = file.read()

    response = openai.Completion.create(
        engine = "gpt-35-turbo",
        prompt= prev_prompt + formatted_question,
        temperature=0.8,
        max_tokens=50,
        top_p=0.8,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response.get("choices")[0]['text']
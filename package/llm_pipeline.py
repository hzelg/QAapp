import streamlit as st
import openai
from openai import AzureOpenAI
import package.gcsManager as gm
from package.utils import *

try:
    client = AzureOpenAI(api_key=st.secrets["OPEN_AI_KEY"], api_version="2023-12-01-preview", azure_endpoint="https://hkust.azure-api.net")
except:
    st.write("wrong")

# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="https://hkust.azure-api.net")'
# openai.api_base = "https://hkust.azure-api.net"

# OpenAI(base_url="https://hkust.azure-api.net")

def process_question_insights():
    return

def generate_insights():
    if st.session_state["csq_media"] == "[]":
        image_ocr = "N/A"
    else:
        image_ocr = gm.get_image_ocr(st.session_state["csq_media"])
    formatted_question = format_question_input(st.session_state["course_info"], st.session_state["csq_title"], st.session_state["csq_body"], image_ocr)
    response = submit_question(formatted_question)
    return response

def display_question_insights(question_id): # Display the latest question insights
    with st.container(border = True):
        col1, col2 = st.columns([3,1])
        with col1:
            st.subheader("LLM Feedback")
        with col2:
            generate = st.button(label = "Generate Insight", type = "primary")
            if generate:
                generate_insights()

        gm.get_all_que_insight(st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])

def submit_question(formatted_question):
    prev_prompt = ""
    with open("prompt.txt", "r") as file:
        prev_prompt = file.read()

    # st.write(prev_prompt + formatted_question)
    response = client.completions.create(model = "gpt-35-turbo",
        prompt= prev_prompt + "\n \"\"\" " + formatted_question + " \"\"\" ",
        temperature=0.8,
        max_tokens=50,
        top_p=0.8,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return response.choices[0].text
import streamlit as st
import openai
from openai import AzureOpenAI
import package.gcsManager as gm

try:
    client = AzureOpenAI(api_key=st.secrets["OPEN_AI_KEY"], api_version="2023-12-01-preview", azure_endpoint="https://hkust.azure-api.net")
except:
    st.write("wrong")

# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="https://hkust.azure-api.net")'
# openai.api_base = "https://hkust.azure-api.net"

# OpenAI(base_url="https://hkust.azure-api.net")

def process_question_insights():
    return


# def generate_insights():
#     formatted_question = utils.format_question_input(st.session_state["course_info"], question_title, question_body, uploaded_image)
#     response = lp.submit_question(formatted_question)
#     displayer.display_question_insights(response)
#     st.session_state["regenerate_question"] = True

def display_question_insights(question_id): # Display the latest question insights
    with st.container(border = True):
        st.subheader("LLM Feedback")
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
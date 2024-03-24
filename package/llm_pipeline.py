import streamlit as st
import openai
from openai import AzureOpenAI
import package.gcsManager as gm
from package.utils import *
import json

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
            generate = st.button(label = "Generate", type = "primary")
        if generate:
            response = generate_insights()
            st.session_state["csq_insights"] = json.loads(response.split("}")[0]+" \n}")
        data = st.session_state["csq_insights"]
        if data != "":
        # data = {"Type": "Question_Type", "Keywords":"Question_Keywords", "Action Items":"Question_ActionItems", "Insights":"Question_Insights"}
            col3, col4 = st.columns([1,2])
            with col3:
                st.caption("Question Type")
            with col4:
                st.write(data["Question_Type"])
                st.session_state["csq_type"] = data["Question_Type"]
            col5, col6 = st.columns([1,2])
            with col5:
                st.caption("Question Keywords")
            with col6:
                st.write(data["Question_Keywords"])
            col7, col8 = st.columns([1,2])
            with col7:
                st.caption("Question Action Items")
            with col8:
                items = str(data["Question_ActionItems"]).split("|")
                for i in items:
                    st.write(i)

            try:
                insights = data["Question_Insights"]
                st.caption("Question Insights")
                st.write(insights)
                st.write(" ")
            except:
                st.write(" ")
                # except:
        else:
            st.write("")
            #     st.error("Error generating response. Please try later!")
            # gm.post_que_insight()
        # gm.get_all_que_insight(st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])

def submit_question(formatted_question):
    prev_prompt = ""
    with open("prompt.txt", "r") as file:
        prev_prompt = file.read()

    # st.write(prev_prompt + formatted_question)
    response = client.completions.create(model = "gpt-35-turbo",
        prompt= prev_prompt + "\n \"\"\" " + formatted_question + " \"\"\" ",
        temperature=0.8,
        top_p=0.2,
        max_tokens= 150,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return response.choices[0].text

def generate_feedbacks(question_course, question_title, question_body, reply):
    prev_prompt = ""
    with open("reply_prompt.txt", "r") as file:
        prompt = file.read()
        prompt = prompt.replace('{quesion_course}', question_course)
        prompt = prompt.replace('{question_title}', question_title)
        prompt = prompt.replace('{question_body}', question_body)
        prompt = prompt.replace('{reply}', reply)
    # st.write(prev_prompt + formatted_question)
    response = client.completions.create(model = "gpt-35-turbo",
        prompt= prompt,
        temperature=0.8,
        top_p=0.2,
        max_tokens= 150,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return response.choices[0].text

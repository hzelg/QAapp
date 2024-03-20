# For TA: Write Reply
# For Student: Submit A Question

import streamlit as st
import package.utils as utils
import package.llm_pipeline as lp
import package.displayer as displayer
from datetime import datetime
import package.gcsManager as gm
from st_files_connection import FilesConnection
import os

st.set_page_config("Write A Question", "💬", layout="wide")

if not st.session_state.role: #Todo: change to TA
#     st.set_page_config("Write A Question", "💬", layout="wide")


### TA Choose a Question To Answer

    # select a question to reply

    ## **************************************************
    # if st.session_state.question_tr == "None":
    #     st.header("Choose A Question To Reply")
    #     st.write(" ")
    #     st.write(" ")
    #     st.write(" ")
    #     col1, col2 = st.columns([5, 1])

    #     with col1:
    #         st.write(" ")
    #         st.write(" ")
    #         st.button(label = "Proceed", type = "primary")
    #         for i in range(0,5): # The number of loaded question, able to show multiple pages
    #             colx, coly = st.columns([8,1])
    #             with colx:
    #                 utils.question_item()
    #             with coly:
    #                 # st.button(label= "Select", key = f"Select Question {i}", type = "primary")
    #                 st.checkbox(label = "question_tr", key = f"select question {i}", label_visibility= "hidden")
    ## **************************************************
                
    col1, col2 = st.columns([2, 3])
    with col1:
        st.subheader("Question")
        utils.display_question()
    with col2:
        utils.display_write_panel()
        lp.display_question_insights()

elif(st.session_state["role"]):
    # st.write(st.session_state["course_info"])
    st.header("Submit A Question")
    # col1, col2, col3 = st.columns([1, 5,3])

    # with col2:
    st.write(" ")
    st.write(" ")

    conn = st.connection('gcs', type = FilesConnection)
    # def generate_insights():
    #     formatted_question = utils.format_question_input(st.session_state["course_info"], question_title, question_body, uploaded_image)
    #     response = lp.submit_question(formatted_question)
    #     displayer.display_question_insights(response)
    #     st.session_state["regenerate_question"] = True

    def save_draft():
        return
        # TODO
    
    with st.container(border = True):

        question_title = st.text_input(label = "Question Title")
        question_body = st.text_area(label = "Question Body")
        uploaded_image = st.file_uploader("Upload image(s) (Optional)", type = ['png', 'jpg'], accept_multiple_files=True)
        send_to = st.selectbox("Send to:", ("jack_1", "winner_2"))
        for uploaded_file in uploaded_image:
            bytes_data = uploaded_file.read()

        col2_1,col2_2,col2_3 = st.columns([1,2,3])
        with col2_1:
            send = st.button(label = "Send")
        with col2_2:
            save_draft = st.button(label = "Save Draft", type="primary")

        if send:
            gm.post_question(send_to, question_title, question_body, uploaded_image,  st.session_state["course_code"], st.session_state["semester"], st.session_state["role"], st.session_state["userid"])

            # post_question(receiver_id, title, body, media, course_code, semester, role, userid):

        # save_continue = st.button(label = "Continue", visibility = st.session_state["regenerate_question"])
        # regenerate = st.button(label = "Regenerate", type = "primary", visibility = st.session_state["regenerate_question"])

        # if send:
        #     generate_insights()

        # if save_continue:
        #     switch()

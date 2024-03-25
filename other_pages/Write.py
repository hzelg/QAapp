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

if not st.session_state.role:

    if st.session_state["current_selected_question_id"] == "":
        st.write("Select a question in **Question History** to start")
    else:
        current_selected_question_id = st.session_state["current_selected_question_id"]
        title = st.session_state["csq_title"]
        body = st.session_state["csq_body"]
        sender_id = st.session_state["csq_sender_id"]
        time = st.session_state["csq_time"]
        media = st.session_state["csq_media"]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Question")
            displayer.display_question(st.session_state["course_info"], title, body, sender_id, time, media)
            lp.display_question_insights(current_selected_question_id)
        with col2:
            displayer.display_write_panel()
            col3, col4, col5 = st.columns([1,1,2])
            with col3:
                reply_submit = st.button(label = "Submit")
            with col4:
                reply_draft = st.button(label = "Save As Draft")
            if st.session_state["csq_type"] == "Conceptual":
                displayer.reply_improvement_panel()
            if reply_submit:
                gm.post_a_reply(st.session_state["csq_reply"])
                utils.clear_csq()

elif(st.session_state["role"]):
    st.header("Submit A Question")

    st.write(" ")
    st.write(" ")

    conn = st.connection('gcs', type = FilesConnection)

    def save_draft():
        return
        # TODO
    
    with st.container(border = True):

        question_title = st.text_input(label = "Question Title")
        question_body = st.text_area(label = "Question Body")
        uploaded_image = st.file_uploader("Upload image(s) (Optional)", type = ['png', 'jpg'], accept_multiple_files=True)
        TAs = gm.get_TA_lists(st.session_state["course_code"],st.session_state["semester"])
        send_to = st.selectbox("Send to:", tuple(TAs.keys())) # get_TA_lists(course_code, semester, role, userid)
        for uploaded_file in uploaded_image:
            bytes_data = uploaded_file.read()

        col2_1,col2_2,col2_3 = st.columns([1,2,3])
        with col2_1:
            send = st.button(label = "Send")
        with col2_2:
            save_draft = st.button(label = "Save Draft", type="primary")

        if send:
            gm.post_question(TAs[send_to], question_title, question_body, uploaded_image, st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])

            # post_question(receiver_id, title, body, media, course_code, semester, role, userid):

        # save_continue = st.button(label = "Continue", visibility = st.session_state["regenerate_question"])
        # regenerate = st.button(label = "Regenerate", type = "primary", visibility = st.session_state["regenerate_question"])

        # if send:
        #     generate_insights()

        # if save_continue:
        #     switch()

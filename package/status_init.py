import streamlit as st
import pandas as pd

def state_initializer():

    # User Information
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "userid" not in st.session_state:
        st.session_state["userid"] = "TA_1"
    if "auth_status" not in st.session_state:
        st.session_state["auth_status"] = False
    if "email" not in st.session_state:
        st.session_state["email"] = ""
    if "ver_code" not in st.session_state:
        st.session_state["ver_code"] = ""
    if "ver_button_disable" not in st.session_state:
        st.session_state["ver_button_disable"] = False
    if "ver_button_text" not in st.session_state:
        st.session_state["ver_button_text"] = "Send Verification Code"
    if "warning_visibility" not in st.session_state:
        st.session_state["warning_visibility"] = False
    if "regenrate_question" not in st.session_state:
        st.session_state["regenerate_question"] = False

    if "role" not in st.session_state:
        st.session_state["role"] = False
    if "role_name" not in st.session_state:
        st.session_state["role_name"] = "TA"

    if "current_selected_question_id" not in st.session_state:
        st.session_state["current_selected_question_id"] = ""
    if "csq_title" not in st.session_state:
        st.session_state["csq_title"] = ""
    if "csq_body" not in st.session_state:
        st.session_state["csq_body"] = ""
    if "csq_time" not in st.session_state:
        st.session_state["csq_time"] = ""
    if "csq_sender_id" not in st.session_state:
        st.session_state["csq_sender_id"] = ""
    if "csq_media" not in st.session_state:
        st.session_state["csq_media"] = "[]"
    if "csq_reply" not in st.session_state:
        st.session_state["csq_reply"] = ""
    if "csq_insights" not in st.session_state:
        st.session_state["csq_insights"] = ""
    if "csq_type" not in st.session_state:
        st.session_state["csq_type"] = ""

    if "course_info" not in st.session_state:
        st.session_state["course_info"] = "COMP3711 Design and Analysis of Algorithm"
    if "course_code" not in st.session_state:
        st.session_state["course_code"] = "COMP3711"
    if "semester" not in st.session_state:
        st.session_state["semester"] = "23Fall"

    # st.write("status successfully initiated.")
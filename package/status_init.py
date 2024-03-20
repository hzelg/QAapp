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
    # if "question_tr" not in st.session_state:
    #     st.session_state["question_tr"] = "None"
    
    if "course_info" not in st.session_state:
        st.session_state["course_info"] = "COMP3711 Design and Analysis of Algorithm"
    if "course_code" not in st.session_state:
        st.session_state["course_code"] = "COMP3711"
    if "semester" not in st.session_state:
        st.session_state["semester"] = "23Fall"

    st.write("status successfully initiated.")
import streamlit as st
import pandas as pd

def state_initializer():

    # User Information
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "userid" not in st.session_state:
        st.session_state["userid"] = ""
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

    if "role" not in st.session_state:
        st.session_state["role"] = False
    if "question_tr" not in st.session_state:
        st.session_state["question_tr"] = "None"
    

    st.write("status successfully initiated.")
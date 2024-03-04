import streamlit as st
import pandas as pd

def state_initializer():


    # User Information
    if "username" not in st.session_state:
        st.session_state["username"] = " "
    if "userid" not in st.session_state:
        st.session_state["userid"] = " "
    if "auth_status" not in st.session_state:
        st.session_state["auth_status"] = False
    if "email" not in st.session_state:
        st.session_state["email"] = " "
    if "hashed_token" not in st.session_state:
        st.session_state["hashed_token"] = " "

    if "role" not in st.session_state:
        st.session_state["role"] = "None"
    if "question_tr" not in st.session_state:
        st.session_state["question_tr"] = "None"
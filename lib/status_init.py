import streamlit as st
import pandas as pd

def state_initializer():
    if "role" not in st.session_state:
        st.session_state["role"] = "None"
    if "question_tr" not in st.session_state:
        st.session_state["question_tr"] = "None"
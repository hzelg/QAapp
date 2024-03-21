import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
import requests
import PIL
import time
import os
import sys
import streamlit.components.v1 as components
import package.status_init as si
import package.utils as utils
from streamlit_option_menu import option_menu
from st_pages import Page, show_pages, add_page_title


si.state_initializer()

add_page_title()
show_pages(
    [
        Page("🏠_Home.py", "Home", "🏠"),
        Page("other_pages/Write.py", "Write", ":books:"),
        Page("other_pages/Question_History.py", "Question History", "💬"),
        Page("other_pages/Progress_Analytics.py", "Progress Report", "🗺️"),
        Page("other_pages/Support.py", "Support", "❓"),
    ]
)

with st.sidebar:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    on = st.toggle('Change to Student Mode', value = st.session_state["role"])
    # st.text_input(label = 'Course code', key = "course_info")
    st.write("The current course is " + st.session_state.course_info)
    
    # Switch between Student/TA Mode
    if on:  
        st.session_state["role"] = True #student mode
        st.session_state["role_name"] = "Student"
        st.session_state["userid"] = "Student_1"
    else:
        st.session_state["role"] = False #ta mode
        st.session_statep["role_name"] = "TA"
        st.session_state["userid"] = "TA_1"
    utils.display_user_info()

st.subheader("Notifications")

col1, col2 = st.columns([7,5])
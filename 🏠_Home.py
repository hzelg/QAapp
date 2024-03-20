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
# st.set_page_config("Home", "🏠", layout="wide")

# if st.session_state["auth_status"] == False:
#     add_page_title()
#     show_pages(
#         [
#             Page("🏠_Home.py", "Home", "🏠"),
#             Page("other_pages/Support.py", "Support", "❓"),
#         ]
#     )

#     col1, col2 = st.columns([3,1])
#     with col1:
#         st.header("Welcome to HKUST MUTutor!")
#         st.write(" ")
#         utils.display_login_panel()


# if st.session_state["auth_status"] == True:

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
    
    if on:  
        st.session_state["role"] = True #student mode\
        st.session_state["userid"] = "Student_1"
    else:
        st.session_state["role"] = False #ta mode
    utils.display_user_info()

# username read from cookies
# username = "Anne"
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.header(f"Good Morning, {username}")


st.subheader("Notifications")

col1, col2 = st.columns([7,5])
with col1:
    with st.container(border = True):
        st.write(" ")
        for i in range(0,5): # The number of loaded question, able to show multiple pages
            utils.question_item()
        st.write(" ")

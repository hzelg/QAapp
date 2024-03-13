import streamlit as st
from datetime import date
import package.user_auth as ua
import time
import re
import package.image_ocr as ocr


def question_item():
    # with st.container(border = True):
    #     st.write("This is a question loaded from database")
    with st.expander("See explanation"):
        st.write("This is a question loaded from database")


def display_question():
    with st.container(border = True):
        st.write("Lecture 1")
        st.write(str(date.today()))
        st.caption("Selection Sort")
        st.write("Question body")
        display_question_insights()


def display_question_insights():
    with st.container(border = True):
        col1,col2 = st.columns([3,1])
        with col1:
            st.write("Question Insights")
        with col2:
            st.button(label = "Refresh")

def display_write_panel():
    st.subheader("Write Reply")
    st.text_area("Write Your Reply Here")


def display_user_info():
    return
    # logout = st.button(label = "Log Out", type = "primary")

def display_login_panel():
    with st.container(border = True):
        st.write("This is an image or logo")
        st.write(" ")
        st.write("Enter Your HKUST Email")
        col1, col2 = st.columns([4,3])
        with col1:
            st.session_state["email"] = st.text_input(label = "email", on_change = validate_email(), label_visibility = "collapsed") 
            if st.session_state.warning_visibility:
                st.warning("Please input a valid HKUST email", icon="⚠️")
        with col2:
            btn = st.button(label = st.session_state["ver_button_text"], disabled = st.session_state["ver_button_disable"])
        if btn:
            ua.send_verification_code(st.session_state["email"])
        verification_code_input = st.text_input(label = "Verification Code")

        st.write(" ")
        login = st.button(label = "Log In / Sign Up (Auto)")
        if login:
            ua.authenticate_user(st.session_state["email"], st.session_state["ver_code"], verification_code_input)
    
def validate_email():
    if re.match(r'^[a-zA-Z0-9._%+-]+@connect\.ust\.hk$', st.session_state.email, re.IGNORECASE):
        st.session_state["warning_visibility"] = False
        st.session_state["ver_button_disable"] = False
        return
    elif(st.session_state.email == ""):
        return
    else:
        st.session_state["warning_visibility"] = True
        return 
    
def format_question_input(question_course,question_title, question_body, uploaded_images):
    # st.write(uploaded_images)
    if len(uploaded_images) == 0:
        text = f"Question Course: {question_course} \n Question Title: {question_title} \n Question Body: \n {question_body} \n Question Media OCR: N\A"
    else:
        image_ocrs = ""
        for i in (1,len(uploaded_images)+1):
            image_ocrs += f"[fig{i}]:"
            image_ocrs += ocr.image_ocr(uploaded_images[i])
            image_ocrs += "\n"
        
        text = f"Question Course: {question_course} \n Question Title: {question_title} \n Question Body: \n {question_body} \n Question Media OCR: "+image_ocrs
    return text
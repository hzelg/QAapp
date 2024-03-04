import streamlit as st
from datetime import date
import package.user_auth as ua


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
    st.button(label = "Log In", type = "primary")

def display_login_panel():
    with st.container(border = True):
        st.write("This is an image or logo")
        col1, col2 = st.columns([4,3])
        with col1:
            st.session_state["email"] = st.text_input(label = "Enter Your HKUST Email")
        with col2:
            send_code = st.button(label = "Send Verification Code")
            if send_code:
                verification_code_sent = ua.send_verification_code(st.session_state["email"])
        verification_code_input = st.text_input(label = "Verification Code")

        st.write(" ")
        login = st.button(label = "Log In / Sign Up (Auto)")
        if login:
            ua.authenticate_user(st.session_state["email"], verification_code_sent, verification_code_input)
        
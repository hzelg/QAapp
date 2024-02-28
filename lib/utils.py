import streamlit as st
from datetime import date


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
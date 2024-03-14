import streamlit as st
import json



def display_question_insights(response):
    output = json.loads(response)
    with st.container(border = True):
        st.caption("Question Type:") # Type of Question
        st.write(output["Question_Type"])
        st.caption("Question Keywords:") # Keywords that help understand the question context
        st.write(output["Question_Keywords"])
        st.caption("Question Action Items:") # Suggested Action Items
        st.write(output["Question Action Items"])
        if output["Question_Insights"]: # Useful external references
            st.caption("Question Insights:")
            st.write(output["Question_Insights"])

    return
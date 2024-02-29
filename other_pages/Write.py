# For TA: Write Reply
# For Student: Submit A Question

import streamlit as st
import lib.utils as utils
import lib.llm_pipeline as lp

## Write A Question for Student


st.set_page_config("Write A Question", "💬", layout="wide")


### TA Choose a Question To Answer
if st.session_state.role == "None": #Todo: change to TA

    # select a question to reply

    ## **************************************************
    # if st.session_state.question_tr == "None":
    #     st.header("Choose A Question To Reply")
    #     st.write(" ")
    #     st.write(" ")
    #     st.write(" ")
    #     col1, col2 = st.columns([5, 1])

    #     with col1:
    #         st.write(" ")
    #         st.write(" ")
    #         st.button(label = "Proceed", type = "primary")
    #         for i in range(0,5): # The number of loaded question, able to show multiple pages
    #             colx, coly = st.columns([8,1])
    #             with colx:
    #                 utils.question_item()
    #             with coly:
    #                 # st.button(label= "Select", key = f"Select Question {i}", type = "primary")
    #                 st.checkbox(label = "question_tr", key = f"select question {i}", label_visibility= "hidden")
    ## **************************************************
                
    col1, col2 = st.columns([2, 3])
    with col1:
        st.subheader("Question")
        utils.display_question()
    with col2:
        utils.display_write_panel()
        lp.display_question_insights()



# after choosing the question, the url will be modified to reflect the current question.
            





### Student Submit A New Question
if st.session_state.role == "Student":
    st.header("Submit A Question")
    col1, col2, col3 = st.columns([1, 5,3])

    with col2:
        st.write(" ")
        st.write(" ")
        with st.container(border = True):
            st.text_input(label = "Title")
            st.text_input(label = "Category")
            st.text_area(label = "Body")
            option = st.selectbox(label = "Send to", options=('Email', 'Home phone', 'Mobile phone'))
            col2_1,col2_2,col2_3 = st.columns([1,2,4])
            with col2_1:
                st.button(label = "Send")
            with col2_2:
                st.button(label = "Save Draft", type="primary")
            
    def submit_question():
        return
        # TODO

    def save_draft():
        return
        # TODO
    

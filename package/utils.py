import streamlit as st
from datetime import date
import package.user_auth as ua
import time
import re
# import package.gcsManager as gm

# def question_item(title, body, course_info, sent_user, time):
#     with st.expander(label = f"{title}"):
#         st.write(f"{course_info} - Question from **{sent_user}** [{time}]")
#         st.caption("Title")
#         st.write(title)
#         st.caption("Body")
#         st.write(body)


# def display_question(course_info, title, body, sender_id, time):
#     sender_username = gm.get_username(sender_id)
#     question_item(title, body, course_info, sender_username, time)


# def display_question_insights():
#     with st.container(border = True):
#         col1,col2 = st.columns([3,1])
#         with col1:
#             st.write("Question Insights")
#         with col2:
#             st.button(label = "Refresh")

def display_write_panel():
    st.subheader("Write Reply")
    st.text_area("Write Your Reply Here")


def display_user_info():
    return

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
    

def format_question_input(question_course,question_title, question_body, image_ocr):
    text = f"\"Question Course\": {question_course} \n \"Question Title\": {question_title} \n \"Question Body\": \n {question_body} \n \"Question Media OCR\": {image_ocr} \n\n System Output: \n"
    return text

def clear_csq():
    st.session_state["current_selected_question_id"] = ""
    st.session_state["current_selected_question_id"] = ""
    st.session_state["csq_title"] = ""
    st.session_state["csq_body"] = ""
    st.session_state["csq_time"] = ""
    st.session_state["csq_sender_id"] = ""
    st.session_state["csq_media"] = "[]"
    st.session_state["csq_reply"] = ""
    st.session_state["csq_insights"] = ""
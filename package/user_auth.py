import pickle
from pathlib import Path

# from flask import Flask, render_template, request, redirect, url_for
# from flask_mail import Mail, Message
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import streamlit_authenticator as stauth
import re
from streamlit_extras.switch_page_button import switch_page

def send_verification_code(email):
    st.session_state["ver_button_disable"] = True
    if st.session_state.ver_code != "":
        return
    if email == "" or (not re.match(r'^[a-zA-Z0-9._%+-]+@connect\.ust\.hk$', email, re.IGNORECASE)):
        return 
    else:
        try:
            st.session_state["ver_button_disable"] = True
            code = str(random.randint(100000, 999999))
            st.session_state["ver_code"] = code

            subject = "Verification Code"
            message = f"Your verification code is: {code}"

            msg = MIMEMultipart()
            msg["From"] = st.secrets["EMAIL_ADDRESS"]
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

        # Replace the following with your SMTP server detail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_TOKEN"])
            server.send_message(msg)
            server.quit()
        except:
            st.write("code sent failed")

        # st.session_state["ver_button_disable"] == True
        st.caption("If you didn't receive the code, please check your junk mail.")
        return code

def authenticate_user(email, verification_code_sent ,verification_code_input):
    st.write(verification_code_input)
    st.write(verification_code_sent)
    if verification_code_sent == verification_code_input:
        st.success("Authentication success! Now redirecting to your portal...")
        st.session_state.auth_status = True
        st.session_state.ver_code == ""
        st.session_state["ver_button_disable"] == False
        # switch_page("Home")
        # switch_page("Write")

    else:
        st.warning("Entered wrong verification code.")
        st.session_state.auth_status = False
    return

    
def logout():
    clean_session_state()
    switch_page("Home")
    return 

def clean_session_state():
    st.session_state["username"] = ""
    st.session_state["userid"] = ""
    st.session_state["auth_status"] = False
    st.session_state["email"] = ""
    st.session_state["ver_code"] = ""
    st.session_state["ver_button_disable"] = False
    st.session_state["ver_button_text"] = "Send Verification Code"
    st.session_state["warning_visibility"] = False
    st.session_state["role"] = "None"
    st.session_state["question_tr"] = "None"
    return 
    
# def disable_button():
#     st.session_state["ver_button_disable"] = True
#     return
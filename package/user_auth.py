import pickle
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import streamlit_authenticator as stauth

app = Flask(__name__)


def send_verification_code(email):
    code = str(random.randint(100000, 999999))
    subject = "Verification Code"
    message = f"Your verification code is: {code}"

    msg = MIMEMultipart()
    msg["From"] = st.secrets["EMAIL_ADDRESS"]
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Replace the following with your SMTP server details
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_TOKEN"])
    server.send_message(msg)
    server.quit()

def authenticate_user(email, verification_code_sent ,verification_code_input):
    if verification_code_sent == verification_code_input:
        st.success("Authentication success! Now redirecting to your portal...")
        st.session_state.auth_status = True
        st.session_state.hashed_token = stauth.Hasher(st.session_state["email"]).generate()
        authenticator = stauth.Authenticate(st.session_state["email"], st.session_state.hashed_token, cookie_expiry_days= 10)
    else:
        st.warning("Entered wrong verification code.")
        st.session_state.auth_status = False
    return
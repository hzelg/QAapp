# Support Page

import streamlit as st
from streamlit_extras.app_logo import add_logo
import package.utils as utils



st.set_page_config("Support", "💬", layout="wide")
add_logo("./media/logo.png", height= 50)
utils.load_css()

st.header("About")
st.header("Resources")
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
import lib.status_init as si
import lib.utils as utils

si.state_initializer()
st.set_page_config("Home", "🏠", layout="wide")


# username read from cookies
username = "Anne"
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.header(f"Good Morning, {username}")


st.subheader("Notifications")

col1, col2 = st.columns([7,5])
with col1:
    with st.container(border = True):
        st.write(" ")
        for i in range(0,5): # The number of loaded question, able to show multiple pages
            utils.question_item()
        st.write(" ")
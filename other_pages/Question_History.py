# For TA: View All Received Question
# For Student: View All Submitted Question


# Read the Database every 5 seconds for updates


import streamlit as st
from streamlit_pills import pills
# from ..lib.utils import *
import package.utils as utils

st.set_page_config("My Questions", "💬", layout="wide")

# read data from database and display as expander
CATEGORY_NAMES = {
    "pending": "Pending",
    "completed": "Completed",
    "drafted": "Drafted",
}

CATEGORY_ICONS = [
    "🟡",
    "🟢",
    "🔘"]

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

col1, col2 = st.columns([2, 1])
search = col1.text_input("Search", placeholder='e.g. "image" or "text" or "card"')
if search:
    print(f"Search term: {search}")
sorting = col2.selectbox(
    "Sort by", ["Default", "📅 Newest"]
)

category = pills(
    "Category",
    list(CATEGORY_NAMES.keys()),
    CATEGORY_ICONS,
    index=None,
    format_func=lambda x: CATEGORY_NAMES.get(x, x),
    label_visibility="collapsed",
)

# if "screen_width" in st.session_state and st.session_state.screen_width < 768:
st.write("")
# For TA: View All Received Question
# For Student: View All Submitted Question
# Read the Database every 5 seconds for updates

import streamlit as st
from streamlit_pills import pills
import package.gcsManager as gm
import package.utils as utils
from streamlit_pagination import pagination_component

st.set_page_config("My Questions", "💬", layout="wide")

# read data from database and display as expander
if st.session_state["role"] == True:
    CATEGORY_NAMES = {
        "pending": "Sent",
        "completed": "Completed",
        "drafted": "Drafted",
    }
    CATEGORY_ICONS = [
    "🟡",
    "🟢",
    "🔘"]

else:
    CATEGORY_NAMES = {
        "pending": "Received",
        "completed": "Answered",
    }
    CATEGORY_ICONS = [
    "🟡",
    "🟢"]


def icon(emoji: str):
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

st.write(category)

role_name = utils.get_role_name(st.session_state["role"])
questions = gm.get_all_question(st.session_state["course_code"], st.session_state["semester"], role_name, st.session_state["userid"])

if category != None:
    filtered_questions = questions[questions["status"] == category]
    if len(filtered_questions) == 0:
        st.write("There is no question in this status.")
    else:
        # st.write(filtered_questions)
        with st.container(border = True):
            st.write(" ")
            for i in range(0,len(filtered_questions)): # The number of loaded question, able to show multiple pages
                utils.question_item(str(filtered_questions.loc[i, 'title']),str(filtered_questions.loc[i, 'body']), st.session_state["course_info"], gm.get_username(filtered_questions.loc[i, 'sender_id']), filtered_questions.loc[i, 'time'] )
                # question_item(title, body, course_code, sent_user, time):
            st.write(" ")
else:
    st.write(questions)



# st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
# # if "screen_width" in st.session_state and st.session_state.screen_width < 768:
# st.write("")

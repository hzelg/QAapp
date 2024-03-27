# For TA: View All Received Question
# For Student: View All Submitted Question
# Read the Database every 5 seconds for updates

import streamlit as st
from streamlit_pills import pills
import package.gcsManager as gm
import package.utils as utils
from streamlit_pagination import pagination_component
from streamlit_extras.switch_page_button import switch_page
import package.displayer as displayer
from streamlit_extras.app_logo import add_logo


st.set_page_config("My Questions", "💬", layout="wide")
add_logo("./media/logo.png", height= 50)
utils.load_css()

# read data from database and display as expander
if st.session_state["role"] == True:
    CATEGORY_NAMES = {
        "sent": "Sent",
        "completed": "Completed",
        "drafted": "Drafted",
    }
    CATEGORY_ICONS = [
    "🟡",
    "🟢",
    "🔘"]

else:
    CATEGORY_NAMES = {
        "sent": "Received",
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

questions = gm.get_all_question(st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])

if category != None:
    filtered_questions = questions[questions["status"] == category]
    if len(filtered_questions) == 0:
        st.write("There is no question in this status.")
    else:
        with st.container(border = True):
            st.write(" ")
            for i in range(0,len(filtered_questions)): 
                _user_name = gm.get_username(str(filtered_questions.loc[i, 'sender_id']))
                with col1:
                    displayer.question_item(str(filtered_questions.loc[i, 'title']), str(filtered_questions.loc[i, 'body']), st.session_state["course_info"], _user_name, filtered_questions.loc[i, 'time'], filtered_questions.loc[i, 'media'])
                with col2:
                    if questions.loc[i, 'status'] == "Received":
                        if st.session_state["role"] == False:
                            write_answer = st.button(label = f"Answer_{i}")
                            if write_answer:
                                switch_page("Write")
                                st.query_params["question_id"] = questions.loc[i, 'postid']
                    st.button(label = "View")
                st.write(" ")
else:
    with st.container(border = True):
        st.write(st.session_state["role_name"])
        st.write(st.session_state["userid"])
        st.write(questions)
        for i in range(0,len(questions)): # The number of loaded question, able to show multiple pages
            st.write(str(questions.loc[i, 'sender_id']))
            _user_name = gm.get_username(str(questions.loc[i, 'sender_id']))
            col1, col2 = st.columns([3,1])
            with col1:
                displayer.question_item(str(questions.loc[i, 'title']), str(questions.loc[i, 'body']), st.session_state["course_info"], _user_name, questions.loc[i, 'time'], questions.loc[i, 'media'])
            with col2:
                if questions.loc[i, 'status'] == "sent":
                    write_answer = st.button(label = "Answer")
                    if write_answer:
                        st.session_state["current_selected_question_id"] = questions.loc[i, 'postid']
                        st.session_state["csq_title"] = questions.loc[i, 'title']
                        st.session_state["csq_body"] = questions.loc[i, 'body']
                        st.session_state["csq_time"] = questions.loc[i, 'time']
                        st.session_state["csq_media"] = questions.loc[i, 'media']
                        st.session_state["csq_sender_id"] = questions.loc[i, 'sender_id']
                                                # st.query_params["question_id"] = 
                        switch_page("Write")
                st.button(label = "View")
        st.write(" ")


# st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
# # if "screen_width" in st.session_state and st.session_state.screen_width < 768:
# st.write("")

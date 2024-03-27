import streamlit as st
import json
import package.gcsManager as gm
import package.llm_pipeline as lp
from st_keyup import st_keyup

def question_item(title, body, course_info, sent_user, time, media):
    with st.expander(label = f"**{title}**", expanded = True):
        st.write(f"Question from **{sent_user}**")
        time_info = f"<span class='text_purple'>{time.split(' ')[0]}</span>"
        st.markdown(time_info, unsafe_allow_html=True)
        st.caption("Title")
        st.write(f"**{title}**")
        st.caption("Body")
        st.write(body)
        if media != "[]":
            media_files = json.loads(media)
            st.write(media_files)
            for i in media_files:
                st.caption("Media")
                q_media = gm.get_media(i)
                st.image(q_media)

def display_question(course_info, title, body, sender_id, time, media):
    sender_username = gm.get_username(sender_id)
    question_item(title, body, course_info, sender_username, time, media)


def display_question_insights(question_id): # Display the latest question insights
    with st.container(border = True):
        col1, col2 = st.columns([3,1])
        with col1:
            st.subheader("LLM Feedback")
        with col2:
            generate = st.button(label = "Generate", type = "primary")
        if generate:
            # try:   
            response = lp.generate_insights()
            st.session_state["csq_processed"] = json.loads(response.split("<End>")[0])
            data = st.session_state["csq_processed"]
            if data != "":
            # data = {"Type": "Question_Type", "Keywords":"Question_Keywords", "Action Items":"Question_ActionItems", "Insights":"Question_Insights"}
                col3, col4 = st.columns([1,2])
                with col3:
                    st.caption("Question Type")
                with col4:
                    # st.write(data["Question_Type"])
                    q_type = f"<span class = 'text_red'>{data['Question_Type']}</span>"
                    st.markdown(q_type, unsafe_allow_html=True)
                    st.session_state["csq_type"] = data["Question_Type"]
                col5, col6 = st.columns([1,2])
                with col5:
                    st.caption("Question Keywords")
                with col6:
                    # st.write(data["Question_Keywords"])
                    q_keywords = f"<span class = 'text_red'>{data['Question_Keywords']}</span>"
                    st.markdown(q_keywords, unsafe_allow_html=True)
                col7, col8 = st.columns([1,2])
                with col7:
                    st.caption("Question Action Items")
                with col8:
                    items = str(data["Question_ActionItems"]).split("|")
                    for i in items:
                        st.write(i)
        
                if data["Question_Insights"]: # Useful external references
                    st.caption("Question Insights:")
                    list_of_insights = data["Question_Insights"].split("|")
                    for i in list_of_insights:
                        st.write(i)
                else:
                    st.write("")
            # except:
            #     st.warning("Something wrong with the server...Please try again later!", icon = "⚠️")

def display_write_panel():
    st.subheader("Your Reply")
    st.caption("Please write your answer here!")
    reply_content = st.text_area("Start to write your reply.", key = "csq_reply")
    st.write(f'{len(reply_content)} characters.')

# def display_question_insights(question_id): # Display the latest question insights
#     with st.container(border = True):
#         st.subheader("LLM Feedback")
#         gm.get_all_que_insight(st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])

def display_reply_feedbacks(feedbacks):
    if feedbacks == "":
        return
    else:
        task_fulfillment = feedbacks[0]["Rating"]
        tf_feedback = feedbacks[0]["Feedback"]
        clarity = feedbacks[1]["Rating"]
        cl_feedback = feedbacks[1]["Feedback"]
        politeness = feedbacks[2]["Rating"]
        politeness_feedback = feedbacks[2]["Feedback"]
        pedagogy_feedback = feedbacks[3]["Suggested"]
        pedagogy_example = feedbacks[3]["Example"]

        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            st.caption("Task Fulfillment")
            feedback = f"<div> <span class='highlight myblue'>@{task_fulfillment}</span><br/>"
            st.markdown(feedback, unsafe_allow_html=True)
            st.write(tf_feedback)

        with col2:
            st.caption("Clarity")
            feedback = f"<div> <span class='highlight mygreen'>@{clarity}</span><br/>"
            st.markdown(feedback, unsafe_allow_html=True)
            # st.write(clarity)
            st.write(cl_feedback)

        with col3:
            st.caption("Politeness & Friendliness")
            feedback = f"<div> <span class='highlight myyellow'>@{politeness}</span><br/>"
            st.markdown(feedback, unsafe_allow_html=True)
            # st.write(politeness)
            st.write(politeness_feedback)

        with col4:
            st.caption("Pedagogy")
            st.write(pedagogy_feedback)
            st.write(pedagogy_example)

def reply_improvement_panel():
    question_title = st.session_state["csq_title"]
    question_body = st.session_state["csq_body"]
    question_media = st.session_state["csq_media"]
    reply = st.session_state["csq_reply"]

    with st.container(border = True):
        get_feedbacks = st.button(label = "Get Feedbacks", type = "primary")
        clear = st.button(label = "Clear")
        if get_feedbacks:
            feedbacks = lp.generate_feedbacks(question_title, question_body, question_media, reply)
            display_reply_feedbacks(feedbacks)
        if clear:
            feedbacks = ""
            display_reply_feedbacks(feedbacks)

    
def display_current_course():
    on = st.toggle('Change to Student Mode', value = st.session_state["role"])
    course_info = f"You are in <span class='highlight course'>{st.session_state.course_code}</span>"
    st.markdown(course_info, unsafe_allow_html=True)
    # st.write("The current course is " + st.session_state.course_info)
    if on:  
        st.session_state["role"] = True #student mode
        st.session_state["role_name"] = "Student"
        st.session_state["userid"] = "Student_1"
        role_info = f"Your role: <span class = 'highlight myblue'>{st.session_state['role_name']}</span>"
        st.markdown(role_info, unsafe_allow_html=True)
    else:
        st.session_state["role"] = False #ta mode
        st.session_state["role_name"] = "TA"
        st.session_state["userid"] = "TA_1"
        role_info = f"Your role: <span class = 'highlight myblue'>{st.session_state['role_name']}</span>"
        st.markdown(role_info, unsafe_allow_html=True)
    
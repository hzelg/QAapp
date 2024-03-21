import streamlit as st
import json
import package.gcsManager as gm
import llm_pipeline as lp

def question_item(title, body, course_info, sent_user, time):
    with st.expander(label = f"{title}"):
        st.write(f"{course_info} - Question from **{sent_user}** [{time}]")
        st.caption("Title")
        st.write(title)
        st.caption("Body")
        st.write(body)


def display_question(course_info, title, body, sender_id, time):
    sender_username = gm.get_username(sender_id)
    question_item(title, body, course_info, sender_username, time)


def display_question_insights(question_id):
    with st.container(border = True):
        st.subheader("LLM Feedback")

        # display existing question insights: latest or no.
        output = gm.get_latest_ques_insight(question_id)
        others = gm.get_a_que_insight(question_id)
                # paginator for existing question insights.

        generate = st.button(label = "Generate question insights")
        if generate:
            response = lp.generate_question_insights(question_id)
            output = json.loads(response)

        with st.container(border = True):
            st.caption("Question Type:") # Type of Question
            st.write(output["Question_Type"])
            st.caption("Question Keywords:") # Keywords that help understand the question context
            st.write(output["Question_Keywords"])
            st.caption("Question Action Items:") # Suggested Action Items
            st.write(output["Question Action Items"])
            if output["Question_Insights"]: # Useful external references
                st.caption("Question Insights:")
                st.write(output["Question_Insights"])

        return


# def display_question_insights(question_id): # Display the latest question insights
#     with st.container(border = True):
#         st.subheader("LLM Feedback")
#         gm.get_all_que_insight(st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])
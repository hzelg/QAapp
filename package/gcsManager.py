import streamlit as st
import json
from google.cloud import storage
from st_files_connection import FilesConnection
import pandas as pd
import os
from datetime import datetime


def upload_csv(local_file_name, destination_blob_name):

    bucket_name = "qa_app"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_name)
    return

def post_user_info(_userid, _username, _user_role, course_code, semester):

    try:
        conn = st.connection('gcs', type = FilesConnection)
        existing_users = conn.read(f"qa_app/{course_code}/{semester}/{course_code}_{semester}_Users.csv", input_format="csv")

        new_user_data = [
            {
                "userid": _userid,
                "username": _username,
                "role": _user_role
            }
        ]
        new_user_info = pd.DataFrame(new_user_data)
        df_to_store = pd.concat(
            [existing_users, new_user_info], ignore_index=True
        )
        df_to_store.to_csv("local_new_users.csv",index = False)
        abs_path = os.path.abspath("local_new_users.csv")
        upload_csv(abs_path, f"{course_code}/{semester}/{course_code}_{semester}_Users.csv")

        new_user_post = None
        if _user_role == "Student":
            new_user_post = [
                {
                    "postid": "",
                    "post_type" :"",
                    "sender_id" :"",
                    "receiver_id":"",
                    "title":"",
                    "body":"",
                    "media":"",
                    "status":"",
                }
            ]

        elif(_user_role == "TA"):
            new_user_post = [
                {
                    "postid": "",
                    "post_type" :"",
                    "sender_id" :"",
                    "receiver_id":"",
                    "title":"",
                    "body":"",
                    "media":"",
                    "status":"",
                }
            ]

        new_user_post_template = pd.DataFrame(new_user_post)
        new_user_post_template.to_csv("local_new_posts.csv", index = False)
        abs_path_2 = os.path.abspath("local_new_posts.csv")
        upload_csv(abs_path_2, f"{course_code}/{semester}/{_user_role}/{_userid}_Posts.csv")

        return "Congrats! You account is created successfully!"
    
    except:
        return "Sorry, something wrong with our server. Please try again later."


def get_user_info(_userid, course_code, semester):
    conn = st.connection('gcs', type = FilesConnection)
    existing_users = conn.read(f"qa_app/{course_code}/{semester}/{course_code}_{semester}_Users.csv", input_format="csv")
    user_data = existing_users[existing_users["userid"] == _userid].to_list()
    return user_data


def post_question(receiver_id, title, body, media, course_code, semester, role_name, userid):
    try:
        conn = st.connection('gcs', type = FilesConnection)

        # Update to Student's Posts
        existing_questions = conn.read(f"qa_app/{course_code}/{semester}/{role_name}/{userid}_Posts.csv", input_format="csv", ttl="600")
        df_len = len(existing_questions)
        question_id = f"q_{df_len+1}"
        new_question_data = [
            {
                "postid": question_id,
                "post_type": "q",
                "sender_id": str(st.session_state.userid),
                "receiver_id":str(receiver_id),
                "title": str(title),
                "body": str(body),
                "media": str(media),
                "status": "sent",
            }
        ]
        new_question_info = pd.DataFrame(new_question_data)
        df_to_store = pd.concat(
            [existing_questions, new_question_info], ignore_index=True
        )
        df_to_store.to_csv("local_new_questions.csv",index = False)
        abs_path = os.path.abspath("local_new_questions.csv")
        upload_csv(abs_path, f"{course_code}/{semester}/{role_name}/{userid}_Posts.csv")


        # Update to corresponding TA's Posts
        existing_questions_2 = conn.read(f"qa_app/{course_code}/{semester}/TA/{receiver_id}_Posts.csv", input_format="csv", ttl="600")
        new_question_data_2 = [
            {
                "postid": question_id,
                "post_type": "q",
                "sender_id": str(st.session_state.userid),
                "receiver_id":str(receiver_id),
                "question_id": "",
                "title": str(title),
                "body": str(body),
                "media": str(media),
                "status": "sent",
            }
        ]
        new_question_info_2 = pd.DataFrame(new_question_data_2)
        df_to_store_2 = pd.concat(
            [existing_questions_2, new_question_info_2], ignore_index=True
        )
        df_to_store_2.to_csv("local_new_questions_2.csv",index = False)
        abs_path_2 = os.path.abspath("local_new_questions_2.csv")
        upload_csv(abs_path_2, f"{course_code}/{semester}/TA/{receiver_id}_Posts.csv")

        return st.success("Question submitted successfully!",icon = "✅")
    
    except:
        return st.error("Sorry, something wrong with our server. Please try again later.",icon = "❌")


def get_all_question(course_code, semester, role_name, userid):
    

    conn = st.connection('gcs', type = FilesConnection)
    existing_posts = conn.read(f"qa_app/{course_code}/{semester}/{role_name}/{userid}_Posts.csv", input_format="csv")
    if role_name == "Student":
        return existing_posts
    elif role_name == "TA":
        existing_questions = existing_posts[existing_posts["post_type"]=="q"]
        return existing_questions


def get_a_question(_postid, course_code, semester, role, username):
    existing_questions = get_all_question(course_code, semester, role, username)
    data = existing_questions[existing_questions["postid"] == _postid].to_dict()
    if data["status"] != "deleted":
        return data
    else:
        return None

def get_a_reply():

    return


def get_all_reply(course_code, semester, role, userid):
    conn = st.connection('gcs', type = FilesConnection)
    existing_replies = conn.read(f"qa_app/{course_code}/{semester}/{role}/{userid}_Posts.csv", input_format="csv")
    return existing_replies


def post_a_reply(reply, media, receiver_id, question_id, course_code, semester, role, userid):

    try:
        existing_replies = get_all_reply(course_code, semester, role, userid)
        df_len = len(existing_replies)

        new_reply_data = [
            {
                "postid": f"r_{df_len+1}",
                "post_type": "r",
                "sender_id": str(st.session_state.userid),
                "receiver_id":str(receiver_id),
                "question_id": str(question_id),
                "body": str(reply),
                "media": str(media),
                "status": "sent",
            }
        ]
        new_reply_info = pd.DataFrame(new_reply_data)
        df_to_store = pd.concat(
            [existing_replies, new_reply_info], ignore_index=True
        )
        df_to_store.to_csv("local_new_replies.csv",index = False)
        abs_path = os.path.abspath("local_new_replies.csv")
        upload_csv(abs_path, f"{course_code}/{semester}/{role}/{userid}_Posts.csv")

        return st.success("Question submitted successfully!",icon = "✅")
    
    except:
        return st.error("Sorry, something wrong with our server. Please try again later.",icon = "❌")
    

def get_all_que_insight(course_code, semester, role, userid):
    conn = st.connection('gcs', type = FilesConnection)
    existing_q_insights = conn.read(f"qa_app/{course_code}/{semester}/{role}/{userid}_Insights/{userid}_Question_Insights.csv", input_format="csv")
    return existing_q_insights

def get_all_answer_evaluation(course_code, semester, role, userid):
    conn = st.connection('gcs', type = FilesConnection)
    existing_a_evaluation= conn.read(f"qa_app/{course_code}/{semester}/{role}/{userid}_Insights/{userid}_Answer_Evaluation.csv", input_format="csv")
    return existing_a_evaluation


def post_que_insight(response, _userid, _question_id, course_code, semester, role):

    try:
        existing_insights = get_all_que_insight(course_code, semester, role, _userid)
        df_len = len(existing_insights)

        new_insight_data = [
            {
                "output_id": f"i_{df_len+1}",
                "question_id": _question_id,
                "generated_time": datetime.now(),	
                "q_type": str(response.type),
                "q_keywords": str(response.keywords),
                "q_action_item": str(response.action_item),
                "q_insights": str(response.insights),
                "status": "null",
            }
        ]
        new_insight_info = pd.DataFrame(new_insight_data)
        df_to_store = pd.concat(
            [existing_insights, new_insight_info], ignore_index=True
        )
        df_to_store.to_csv("local_new_insights.csv",index = False)
        abs_path = os.path.abspath("local_new_insights.csv")
        upload_csv(abs_path, f"qa_app/{course_code}/{semester}/{role}/{_userid}_Insights/{_userid}_Question_Insights.csv")

        return "Insights saved successfully."
    
    except:
        return "Sorry, something wrong with our server. Please try again later."


def post_ans_evaluation(response, _userid, _question_id, _answer_id, course_code, semester, role):
    try:
        existing_evaluations = get_all_answer_evaluation(course_code, semester, role, _userid)
        df_len = len(existing_evaluations)

        new_eval_data = [
            {
                "output_id":f"e_{df_len+1}",
                "question_id":_question_id,
                "answer_id":_answer_id,
                "generated_time":datetime.now(),
                "dimension_scores":response.dimension_scores,
                "d1_feedback":response.d1_feedback,
                "d2_feedback":response.d2_feedback,
                "d3_feedback":response.d3_feedback,
                "d4_feedback":response.d4_feedback,
                "overall_feedback":response.overall_feedback,
            }
        ]
        new_eval_info = pd.DataFrame(new_eval_data)
        df_to_store = pd.concat(
            [existing_evaluations, new_eval_info], ignore_index=True
        )
        df_to_store.to_csv("local_new_eval.csv",index = False)
        abs_path = os.path.abspath("local_new_eval.csv")
        upload_csv(abs_path, f"qa_app/{course_code}/{semester}/{role}/{_userid}_Insights/{_userid}_Answer_Evaluation.csv")

        return "Evaluation saved successfully."
    
    except:
        return "Sorry, something wrong with our server. Please try again later."

def get_one_que_insight(_question_id, course_code, semester, role, userid):
    existing_insights = get_all_que_insight(course_code, semester, role, userid)
    list_of_insights = existing_insights[existing_insights["question_id"] == _question_id].to_list()

    return list_of_insights

def get_an_ans_evaluation(_answer_id, course_code, semester, role, userid):
    existing_eval = get_all_answer_evaluation(course_code, semester, role, userid)
    list_of_eval = existing_eval[existing_eval["answer_id"] == _answer_id].to_list()

    return list_of_eval

def get_TA_lists(course_code, semester):
    conn = st.connection('gcs', type = FilesConnection)
    existing_users = conn.read(f"qa_app/{course_code}/{semester}/Users.csv", input_format="csv")
    st.write(existing_users)
    tmp_1 = existing_users[existing_users["user_role"] == "TA"]
    st.write(tmp_1)
    TA_ids = (tmp_1["userid"]).tolist()
    st.write(TA_ids)
    TA_names = existing_users[existing_users["user_role"] == "TA"]["username"].tolist()
    tuples = [(key, value) for i, (key, value) in enumerate(zip(TA_names, TA_ids))]
    res = dict(tuples)
    return res

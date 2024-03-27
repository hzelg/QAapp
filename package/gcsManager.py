import streamlit as st
import json
from google.cloud import storage
from st_files_connection import FilesConnection
import pandas as pd
import os
from datetime import datetime
import requests


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
                    "time":"",
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
                    "time":"",
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
        if len(media) != 0:
            list_of_media = []
            for i in range(0,len(media)):
                list_of_media.append(f"{question_id}_{i}.jpg")
            new_question_data = [
                {
                    "postid": question_id,
                    "post_type": "q",
                    "sender_id": str(st.session_state.userid),
                    "receiver_id":str(receiver_id),
                    "time": datetime.now(),
                    "title": str(title),
                    "body": str(body),
                    "media": str(list_of_media),
                    "status": "sent",
                }
            ]
        else:
            new_question_data = [
                {
                    "postid": question_id,
                    "post_type": "q",
                    "sender_id": str(st.session_state.userid),
                    "receiver_id":str(receiver_id),
                    "time": datetime.now(),
                    "title": str(title),
                    "body": str(body),
                    "media": "[]",
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
        if len(media) != 0:
            for i in range(0,len(media)):
                media_abs_path = os.path.abspath(media[i])
                upload_csv(media_abs_path, f"{course_code}/{semester}/{role_name}/{userid}_media/{question_id}_{i}.jpg") # only one media file is allowed for now.

        # Update to corresponding TA's Posts
        existing_questions_2 = conn.read(f"qa_app/{course_code}/{semester}/TA/{receiver_id}_Posts.csv", input_format="csv", ttl="600")
        if len(media) != 0:
            list_of_media = []
            for i in range(0,len(media)):
                list_of_media.append(f"{question_id}_{i}.jpg")
            
            new_question_data_2 = [
                {
                    "postid": question_id,
                    "post_type": "q",
                    "sender_id": str(st.session_state.userid),
                    "receiver_id":str(receiver_id),
                    "time": datetime.now(),
                    "question_id": "",
                    "title": str(title),
                    "body": str(body),
                    "media": str(list_of_media),
                    "status": "sent",
                }
            ]
        else:
            new_question_data_2 = [
                {
                    "postid": question_id,
                    "post_type": "q",
                    "sender_id": str(st.session_state.userid),
                    "receiver_id":str(receiver_id),
                    "time": datetime.now(),
                    "question_id": "",
                    "title": str(title),
                    "body": str(body),
                    "media": "[]",
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


def get_a_question(_postid, course_code, semester, role_name, userid):
    existing_questions = get_all_question(course_code, semester, role_name, userid)
    data = existing_questions[existing_questions["postid"] == _postid].to_dict()
    if data["status"] != "deleted":
        return data
    else:
        return None

def get_a_reply():

    return


def get_all_reply():
    conn = st.connection('gcs', type = FilesConnection)
    existing_replies = conn.read(f"qa_app/{st.session_state.course_code}/{st.session_state.semester}/{st.session_state.role_name}/{st.session_state.userid}_Posts.csv", input_format="csv")
    return existing_replies


def post_a_reply(reply):

    try:
        existing_replies = get_all_reply()
        df_len = len(existing_replies)

        new_reply_data = [
            {
                "postid": f"r_{df_len+1}",
                "post_type": "r",
                "sender_id": str(st.session_state.userid),
                "receiver_id":str(st.session_state.csq_sender_id),
                "time":datetime.now(),
                "question_id": str(st.session_state.current_selected_question_id),
                "body": str(reply),
                "media": "[]",
                "status": "sent",
            }
        ]
        new_reply_info = pd.DataFrame(new_reply_data)
        existing_replies.loc[existing_replies["postid"] == str(st.session_state.current_selected_question_id), ['status']] = "completed"
        df_to_store = pd.concat(
            [existing_replies, new_reply_info], ignore_index=True
        )
        df_to_store.to_csv("local_new_replies.csv",index = False)
        abs_path = os.path.abspath("local_new_replies.csv")
        upload_csv(abs_path, f"{st.session_state.course_code}/{st.session_state.semester}/{st.session_state.role_name}/{st.session_state.userid}_Posts.csv")

        # Should update student's side, but not for this demo.

        return st.success("Reply submitted successfully!",icon = "✅")
    
    except:
        return st.error("Sorry, something wrong with our server. Please try again later.",icon = "❌")
    

def get_all_que_insight(course_code, semester, role, userid):
    conn = st.connection('gcs', type = FilesConnection)
    existing_q_insights = conn.read(f"qa_app/{course_code}/{semester}/{role}/{userid}_Question_Insights.csv", input_format="csv")
    return existing_q_insights

def get_all_answer_evaluation(course_code, semester, role, userid):
    conn = st.connection('gcs', type = FilesConnection)
    existing_a_evaluation= conn.read(f"qa_app/{course_code}/{semester}/{role}/{userid}_Answer_Evaluation.csv", input_format="csv")
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
        upload_csv(abs_path, f"qa_app/{course_code}/{semester}/{role}/{_userid}_Question_Insights.csv")

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
        upload_csv(abs_path, f"qa_app/{course_code}/{semester}/{role}/{_userid}_Answer_Evaluation.csv")

        return "Evaluation saved successfully."
    
    except:
        return "Sorry, something wrong with our server. Please try again later."

def get_latest_que_insight(_question_id):
    existing_insights = get_all_que_insight(st.session_state["course_code"], st.session_state["semester"], st.session_state["role_name"], st.session_state["userid"])
    tmp = existing_insights[existing_insights["question_id"] == _question_id]
    # output_id, question_id, generated_time, q_type, q_keywords, q_action_item, q_insights, status
    if len(tmp) == 0: # no insights generated:
        st.write("No insights available now.")
    else:
        st.write(tmp)
        # list_types = tmp["q_type"].tolist()
        # list_keywords = tmp["q_keywords"].tolist()
        # list_action_item = tmp["q_action_item"].tolist()
        # list_insights = tmp["q_insights"].tolist()

    return tmp

def get_a_que_insights():
    return

def get_an_ans_evaluation(_answer_id, course_code, semester, role, userid):
    existing_eval = get_all_answer_evaluation(course_code, semester, role, userid)
    list_of_eval = existing_eval[existing_eval["answer_id"] == _answer_id].to_list()

    return list_of_eval

def get_TA_lists(course_code, semester):
    conn = st.connection('gcs', type = FilesConnection)
    existing_users = conn.read(f"qa_app/{course_code}/{semester}/Users.csv", input_format="csv")
    tmp_1 = existing_users[existing_users["user_role"] == "TA"]
    TA_ids = (tmp_1["userid"]).tolist()
    TA_names = existing_users[existing_users["user_role"] == "TA"]["username"].tolist()
    tuples = [(key, value) for i, (key, value) in enumerate(zip(TA_names, TA_ids))]
    res = dict(tuples)
    return res


def get_username(userid):
    # st.write("Getting username...")
    conn = st.connection('gcs', type = FilesConnection)
    existing_users = conn.read(f"qa_app/{st.session_state.course_code}/{st.session_state.semester}/Users.csv", input_format="csv")
    # st.write(existing_users[existing_users["userid"] == userid]["username"].tolist()[0])
    return str(existing_users[existing_users["userid"] == userid]["username"].tolist()[0])

def get_media(media_name):
    conn = st.connection('gcs', type = FilesConnection)
    img = conn.read(f"qa_app/{st.session_state.course_code}/{st.session_state.semester}/Student/{st.session_state.csq_sender_id}/{media_name}")
    return img

def get_img_ocr(media_name):
    image = get_media(media_name)

    r = requests.post("https://api.mathpix.com/v3/text",   
        files={"file": open(image,"rb")},
        data={
            "options_json": json.dumps({
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True
            })
        },
        headers={
            "app_id": st.secrets["APP_ID"],
            "app_key": st.secrets["APP_KEY"]
        }
    )

    return (json.dumps(r.json(), indent=4, sort_keys=True)).text
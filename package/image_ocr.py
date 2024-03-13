import requests
import json
import streamlit as st

def image_ocr(image):

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
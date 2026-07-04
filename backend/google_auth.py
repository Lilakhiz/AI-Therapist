import os
import json
import base64
import requests

import streamlit as st

from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component
from backend.database import (
    create_user,
    get_user,
    get_user_by_id,
    update_user_contact
)

load_dotenv()

oauth = OAuth2Component(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    refresh_token_endpoint="https://oauth2.googleapis.com/token",
    revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
)

def decode_id_token(id_token):

    payload = id_token.split(".")[1]

    payload += "=" * (-len(payload) % 4)

    return json.loads(
        base64.urlsafe_b64decode(payload)
    )

def login():

    result = oauth.authorize_button(
        "Continue with Google",
        redirect_uri="http://localhost:8501",
        scope="openid email profile",
        key="google",
        use_container_width=True,
        icon="https://developers.google.com/identity/images/g-logo.png",
    )

    if not result:
        return

    token = result["token"]

    user = decode_id_token(
        token["id_token"]
    )

    create_user(
    user["sub"],
    user["name"],
    user["email"],
    user["picture"],
    None,
    None
)

    db_user = get_user(user["email"])

    st.session_state.user = {
    "id": db_user["id"],
    "google_id": db_user["google_id"],
    "name": db_user["name"],
    "email": db_user["email"],
    "picture": db_user["picture"],
    "phone": db_user["phone"],
    "emergency_contact": db_user["emergency_contact"],
}


    st.session_state.access_token = token["access_token"]

    st.rerun()

def is_logged_in():

    return "user" in st.session_state

def current_user():

    return st.session_state.get("user")


import requests
import streamlit as st


def logout():

    token = st.session_state.get("access_token")

    if token:

        requests.post(
            "https://oauth2.googleapis.com/revoke",
            params={
                "token": token
            },
        )

    st.session_state.clear()

    st.rerun()
import bcrypt
import streamlit as st

from backend.database import (
    get_connection,
    get_user_by_id,
)


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )


def signup(name, email, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE email=?",
        (email,)
    )

    if cur.fetchone():
        conn.close()
        return False, "Email already exists."

    cur.execute(
        """
        INSERT INTO users(
            name,
            email,
            password_hash
        )
        VALUES(?,?,?)
        """,
        (
            name,
            email,
            hash_password(password)
        )
    )

    conn.commit()
    conn.close()

    return True, "Account created successfully."


def login(email, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cur.fetchone()

    conn.close()

    if user is None:
        return False

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return False

    st.session_state.user = dict(user)

    return True


def logout():

    st.session_state.clear()


def is_logged_in():

    return "user" in st.session_state


def current_user():

    return st.session_state.user
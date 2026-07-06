import streamlit as st
import requests
from datetime import date, datetime
from backend.database import (
    save_chat,
    save_mood,
    get_all_moods,
    save_journal,
    load_journal,
    get_user_by_id,
    update_user_contact,
    get_mood_by_date,
    get_journal_by_date,
    get_chat_by_date,
    clear_chat_history,
    get_connection
)
from collections import Counter
import calendar
from datetime import datetime
from backend.mental_health_cards import get_daily_card
from backend.cbt import(
    get_cbt
)
from backend.auth import (
    login,
    logout,
    is_logged_in,
    current_user,
    signup,
)

st.set_page_config(
    page_title="SafeSpace",
    page_icon="🧠",
    layout="wide"
)


from backend.database import get_user_by_id

if "signup_step" not in st.session_state:
    st.session_state.signup_step = 1


#login
if not is_logged_in():

    st.title("🧠 SafeSpace")
    st.caption("Your AI Mental Health Companion")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            success = login(
                email,
                password
            )

            if success:
                st.success("Welcome back!")
                st.rerun()

            else:
                st.error("Invalid email or password.")

    with tab2:

        if st.session_state.signup_step == 1:

            name = st.text_input(
                "Name",
                key="signup_name"
            )

            email = st.text_input(
                "Email",
                key="signup_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            if st.button(
                "Continue",
                use_container_width=True
            ):

                if password != confirm:
                    st.error("Passwords don't match.")

                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")

                else:

                    conn = get_connection()
                    cur = conn.cursor()

                    cur.execute(
                        "SELECT id FROM users WHERE email=?",
                        (email,)
                    )

                    exists = cur.fetchone()

                    conn.close()

                    if exists:

                        st.error(
                            "An account with this email already exists."
                        )

                    else:

                        st.session_state.pending_name = name
                        st.session_state.pending_email = email
                        st.session_state.pending_password = password

                        st.session_state.signup_step = 2
                        st.rerun()

        else:
            st.success("✅ Email available!")


            if st.button("Create Account", use_container_width=True):
                ok, user = signup(st.session_state.pending_name, st.session_state.pending_email, st.session_state.pending_password)
                if ok:
                    st.success("Account created successfully! Logging you in...")
                    
                    # 1. Clear out step 2 tracking
                    st.session_state.signup_step = 1 
                    
                    # 2. Wipe the widget inputs completely from memory
                    for key in ["signup_name", "signup_email", "signup_password", "signup_confirm", "signup_phone", "pending_name", "pending_email", "pending_password"]:
                        st.session_state.pop(key, None)
                    
                    # 3. Now safely rerun into the dashboard
                    st.rerun()
                else:

                    st.error(user)
                    if st.button("⬅ Back"):

                        #st.session_state.signup_step = 1
                        st.rerun()

    st.stop()

user = current_user()
user_id = user["id"]

from backend.database import load_chat_history

history = load_chat_history(user_id, date.today().isoformat())

st.session_state.chat_history = [
    {
        "role": row["role"],
        "content": row["message"]
    }
    for row in history
]

db_user = get_user_by_id(user_id)

if (
    db_user["phone"] is None
    or
    db_user["emergency_contact"] is None
):

    st.title("📱 Complete Your Profile")

    phone = st.text_input(
        "Your Phone Number",
        placeholder="+919876543210"
    )

    emergency = st.text_input(
        "Emergency Contact Number",
        placeholder="+919812345678"
    )

    if st.button(
        "Save",
        use_container_width=True
    ):

        update_user_contact(
            user_id,
            phone,
            emergency
        )

        updated_user = get_user_by_id(user_id)

        st.session_state.user.update({
            "phone": updated_user["phone"],
            "emergency_contact": updated_user["emergency_contact"],
        })

        st.success("Profile saved!")

       # st.rerun()

    st.stop()


def mood_changed():
    save_mood(
        st.session_state.user["id"],
        st.session_state.mood
    )

import os

BACKEND_URL = st.secrets.get(
    "BACKEND_URL",
    "http://localhost:8000/ask"
)



if "page" not in st.session_state:
    st.session_state.page = "chat"

if "selected_date" not in st.session_state:
    st.session_state.selected_date = None

#session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

#sidebar
with st.sidebar:

    st.title("🧠 SafeSpace")

    st.write(f"### Hi {user['name']}")

    st.caption(user["email"])

    if st.button("🚪 Logout", use_container_width=True):
        logout()

    st.markdown("---")

    st.markdown("###  Daily Mental Health Tip")

    st.warning(get_daily_card())

    st.markdown("---")

    st.markdown("### 🧘 Quick Calm")

    if st.button("🫁 Start Breathing Exercise", use_container_width=True):
        st.session_state.page = "breathing"
        st.rerun()

    st.markdown("---")

    st.selectbox(
        "Current Mood",
        [
            "😊 Happy",
            "😐 Neutral",
            "😔 Sad",
            "😰 Anxious",
            "😡 Angry"
        ],
        key="mood",
        on_change=mood_changed
)

    st.markdown("---")

    if st.button("🗑 Clear Chat", use_container_width=True):
        clear_chat_history(user_id)
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    st.info(
        "SafeSpace offers emotional support.\n\n"
        "It is **not** a replacement for a licensed therapist."
    )

    #mood calender
    st.markdown("---")
    st.subheader("📅 Mood Calendar")

    moods = get_all_moods(user_id)

    # Convert database rows into a dictionary
    mood_dict = {}

    for day, mood in moods:
        mood_dict[day] = mood.split()[0]      # 😊 Happy -> 😊

    today = datetime.today()

    year = today.year
    month = today.month

    st.markdown(
        f"<h4 style='text-align:center'>{calendar.month_name[month]} {year}</h4>",
        unsafe_allow_html=True
    )

    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    cols = st.sidebar.columns(
        7,
        gap="small"
        )

    for col, day in zip(cols, days):
        col.markdown(f"**{day}**")

    month_days = calendar.monthcalendar(year, month)

    for week in month_days:

        cols = st.columns(7)

        for col, day in zip(cols, week):

            with col:

                if day == 0:
                    st.write("")
                    continue

                date_str = f"{year}-{month:02d}-{day:02d}"

                emoji = mood_dict.get(date_str, "")

                is_today = (
                    day == today.day
                    and month == today.month
                    and year == today.year
                )

                label = f"{day}"

                if is_today:
                    label = f"🟢 {day}"

                if st.button(
                    label,
                    key=f"calendar_{date_str}",
                    use_container_width=True
                ):
                    st.session_state.selected_date = date_str

                st.markdown(
                    f"<div style='text-align:center;font-size:22px'>{emoji}</div>",
                    unsafe_allow_html=True
                )


    st.markdown("---")
    st.subheader("📊 Mood Statistics")

    stats = Counter(mood for _, mood in moods)
    total = sum(stats.values())

    all_moods = [
        "😊 Happy",
        "😐 Neutral",
        "😔 Sad",
        "😰 Anxious",
        "😡 Angry"
    ]

    for mood in all_moods:
        count = stats.get(mood, 0)
        percent = count / total if total else 0
        st.write(f"{mood} ({count})")
        st.progress(percent)

    st.markdown("---")

    if st.button("📝 Daily Journal", use_container_width=True):
        st.session_state.page = "journal"

    if st.session_state.selected_date:

        st.markdown("---")

        st.subheader(
            f"📅 {datetime.strptime(st.session_state.selected_date,'%Y-%m-%d').strftime('%d %B %Y')}"
        )

        mood = get_mood_by_date(
            user_id,
            st.session_state.selected_date
        )

        journal = get_journal_by_date(
            user_id,
            st.session_state.selected_date
        )

        chats = get_chat_by_date(
            user_id,
            st.session_state.selected_date
        )


        # Mood

        st.markdown("### 😊 Mood")

        if mood:
            st.success(mood)
        else:
            st.info("No mood recorded.")


        # Journal

        st.markdown("### 📝 Journal")

        if journal:
            st.write(journal)
        else:
            st.info("No journal entry.")


        # Chat History

        st.markdown("### 💬 Chat History")

        if chats:

            avatars = {
                "user": "🙂",
                "assistant": "🧠"
            }

            for chat in chats:

                with st.chat_message(
                    chat["role"],
                    avatar=avatars[chat["role"]]
                ):
                    st.markdown(chat["message"])

        else:

            st.info("No conversations recorded.")
        

if st.session_state.page == "chat":
    #header
    st.markdown(
    """
    <div style='text-align:center;'>

    <h1>🧠 SafeSpace</h1>

    <h4>Your AI Mental Health Companion</h4>

    </div>
    """,
    unsafe_allow_html=True
    )

    #welcome screen
    if not st.session_state.chat_history:

        st.markdown(
        """
        <div style="text-align:center;padding-top:40px">

        <h2>👋 Welcome!</h2>

        <p>Everything starts with one message.</p>

        <br>

        📚 College Stress<br>
        😔 Anxiety<br>
        ❤️ Relationships<br>
        😴 Sleep Problems<br>
        💼 Career Pressure<br>
        🌱 Self Improvement

        </div>
        """,
        unsafe_allow_html=True
        )

    #chat history
    avatars = {
        "user": "🙂",
        "assistant": "🧠"
    }

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"],
            avatar=avatars[message["role"]]
        ):
            st.markdown(message["content"])

    #chat input
    prompt = st.chat_input("💬 What's on your mind today?")

    #backend logic
    if prompt:

        # Show user immediately
        st.session_state.chat_history.append({
            "role":"user",
            "content":prompt
        })
        save_chat(user_id, "user", prompt)

        save_mood(
                    st.session_state.user["id"],
                    st.session_state.mood
                )

        with st.chat_message("user", avatar="🙂"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🧠"):
            thinking = st.empty()
            thinking.markdown("💭 SafeSpace is thinking...")

            try:
                res = requests.post(
                    BACKEND_URL,
                    json={
                            "user_id": user_id,
                            "message": prompt
                        },
                    timeout=60
                )

                res.raise_for_status()
                data = res.json()
                response = data["response"]
                therapists = data.get("therapists", [])

                cbt = data.get("cbt")

                if therapists:
                    response += "\n\n---\n## 📍 Nearby Therapists\n"

                    for t in therapists:
                        response += f"""

                        ### 🧠 {t['name']}

                        ⭐ {t['rating']}

                        📍 {t['address']}

                        📞 {t['phone']}

                        """

                        if t["website"]:
                            response += f"\n🌐 {t['website']}"
                            response += f"\n🗺️ {t['maps']}"
                if cbt:
                    response += f"""
                        ---
                        ## {cbt['title']}
                        {cbt['exercise']}
                        """

                thinking.markdown(response)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

                #save_chat("assistant", response)

                save_chat(user_id, "assistant", response)

            except Exception as e:
                thinking.error(str(e))

    #footer
    st.markdown("---")

    st.caption(
    "SafeSpace is an AI companion designed for emotional support.\n\n"
    "If you're in immediate danger, contact your local emergency services."
    )
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center; color:gray; font-size:13px;">
            © 2026 Akhilesh • SafeSpace v1.0
        </div>
        """,
        unsafe_allow_html=True
        )

elif st.session_state.page == "journal":
    st.title("📝 Daily Journal")

    st.caption(datetime.today().strftime("%d %B %Y"))

    st.markdown("---")

    prompts = {

                "😊 Happy":
                "What made you smile today?",

                "😐 Neutral":
                "Describe your day in three words.",

                "😔 Sad":
                "What weighed on your mind today?",

                "😰 Anxious":
                "What is one thing worrying you right now?",

                "😡 Angry":
                "What made you feel this way today?"

                }

    prompt = prompts[st.session_state.mood]

    st.markdown("### ✨ Reflection Prompt")

    st.info(prompt)

    journal = st.text_area(
        "Dear Diary...",
        value=load_journal(user_id),
        height=250,
        placeholder="Write whatever is on your mind..."
)

    c1,c2 = st.columns(2)

    with c1:

        if st.button("💾 Save Journal"):
            save_journal(
                user_id,
                st.session_state.mood,
                prompt,
                journal
            )
            st.toast("Entry saved successfully ✨")

    with c2:

        if st.button("⬅ Back"):

            st.session_state.page = "chat"

            st.rerun()
else:
    st.title("🫁 Guided Breathing")
    st.caption("Take one minute for yourself.")

    st.markdown("""
                    <style>

                    @keyframes breathe {

                        0%{
                            transform:scale(0.8);
                        }

                        50%{
                            transform:scale(1.35);
                        }

                        100%{
                            transform:scale(0.8);
                        }

                    }

                    .breath-circle{

                        width:180px;
                        height:180px;

                        border-radius:50%;

                        background:linear-gradient(135deg,#3b82f6,#60a5fa);

                        margin:auto;

                        animation:breathe 8s infinite ease-in-out;

                        box-shadow:0px 0px 40px rgba(59,130,246,.5);

                    }

                    </style>
                    """, unsafe_allow_html=True)
    
    st.markdown("""
                <div class="breath-circle"></div>
                """, unsafe_allow_html=True
                )
    
    st.markdown("---")

    if st.button("⬅ Back", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()
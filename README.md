# 🧠 SafeSpace – AI Mental Health Companion

> An intelligent AI-powered mental wellness platform that combines conversational therapy, mood tracking, journaling, and crisis detection into one secure application.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue)
![Streamlit OAuth](https://img.shields.io/badge/Auth-Streamlit%20OAuth-orange)

---

## 📖 Overview

SafeSpace is an AI-powered mental health companion designed to provide users with a private and supportive environment to reflect on their emotions, track mental wellness, and receive AI-guided conversations.

Unlike a traditional chatbot, SafeSpace provides **persistent user accounts**, **daily mood tracking**, **journaling**, **conversation history**, and **crisis detection** with emergency contact support.

Demo : https://safespace-by-akhilesh.streamlit.app/

---

# ✨ Features

### 🤖 AI Therapist

- Context-aware conversations
- Persistent memory across sessions
- Personalized responses
- Multi-turn conversations

---

### 🔐 Secure Streamlit Authentication

- Streamlit OAuth Login
- User-specific data
- Secure session management

---

### 😊 Mood Tracking

- Daily mood selection
- Mood calendar
- Mood history
- Mood statistics

---

### 📖 Daily Journal

- One journal entry per day
- Linked with mood
- AI-generated journal prompts

---

### 📅 Mental Health Timeline

Click any day on the calendar to view:

- Mood
- Journal entry
- Chat history

Everything is stored per user.

---

### 🚨 Crisis Detection

When severe distress is detected:

- AI identifies high-risk conversations
- Emergency contact is notified using Twilio

---

### 📱 User Profiles

Each user stores:

- Streamlit Account
- Phone Number
- Emergency Contact

---

### 💾 Persistent Memory

Unlike temporary chatbot memory:

- Conversations are stored in SQLite
- AI reloads previous conversations
- Works after page refresh
- Works after server restart

---

# 🏗️ Architecture

```
                    Streamlit OAuth
                          │
                          ▼
                  Streamlit Frontend
                          │
             REST API Requests
                          │
                          ▼
                 FastAPI Backend
                          │
      ┌───────────┬────────────┬─────────────┐
      │           │            │
      ▼           ▼            ▼
 AI Therapist   Crisis      Database
                Detection
      │
      ▼
 SQLite Database
      │
      ├── Users
      ├── Chat History
      ├── Mood History
      └── Journal Entries
```

---

# 🛠️ Tech Stack

## Frontend

- Streamlit

## Backend

- FastAPI

## AI
- Groq LLM

## Authentication

- streamlit-oauth

## Database

- SQLite

## APIs

- Twilio
- Streamlit OAuth

---

# 📂 Project Structure

```
SafeSpace/

│
├── backend/
│   ├── database.py
│   ├── therapist.py
│   ├── crisis.py
│   ├── emergency.py
│   ├── therapist_locator.py
│   ├── mental_health_cards.py
│   ├── location.py
│   ├── config.py
│   └── main.py
│
├── frontend.py
├── Streamlit_auth.py
├── .env
├── pyproject.toml
└── README.md
```

---

# 🗄️ Database Design

```
Users
-----
id
Streamlit_id
name
email
picture
phone
emergency_contact

Chat History
------------
id
user_id
role
message
timestamp

Mood History
------------
id
user_id
date
mood

Journal
-------
id
user_id
date
mood
prompt
journal
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/SafeSpace.git

cd SafeSpace
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env`

```env
Streamlit_CLIENT_ID=

Streamlit_CLIENT_SECRET=

GROQ_API_KEY=

TWILIO_ACCOUNT_SID=

TWILIO_AUTH_TOKEN=

TWILIO_PHONE_NUMBER=
```

---

## Create Database

```bash
python backend/database.py
```

---

## Start Backend

```bash
uvicorn backend.main:app --reload
```

---

## Start Frontend

```bash
streamlit run frontend.py
```

---

# 🔒 Privacy

- User-specific encrypted sessions
- Streamlit Authentication
- Personal data isolated per user
- No shared conversations

---

# 📈 Future Improvements

- PostgreSQL
- Docker
- Conversation History
- RAG using Mental Health Knowledge Base
- Therapist Recommendation System
- Voice Conversations
- Emotion Detection from Voice
- Mobile Application
- Analytics Dashboard

---

# 👨‍💻 Author

**Akhilesh**

Computer Science Undergraduate

Manipal Institute of Technology Bengaluru

GitHub:
https://github.com/yourusername

---

# ⭐ If you found this project interesting, consider giving it a star!

import sqlite3

DB_NAME = "backend/safespace.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()


    # Chat History
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS chat_history(

                            id INTEGER PRIMARY KEY AUTOINCREMENT,

                            user_id INTEGER NOT NULL,

                            role TEXT NOT NULL,

                            message TEXT NOT NULL,

                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

                            FOREIGN KEY(user_id)
                            REFERENCES users(id)
                            ON DELETE CASCADE

                        )
                """)


    # Mood History
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mood_history(

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        user_id INTEGER NOT NULL,

                        date TEXT NOT NULL,

                        mood TEXT NOT NULL,

                        UNIQUE(user_id, date),

                        FOREIGN KEY(user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE

                    )
                    """)


    # Journal
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS journal(

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        user_id INTEGER NOT NULL,

                        date TEXT NOT NULL,

                        mood TEXT,

                        prompt TEXT,

                        journal TEXT,

                        UNIQUE(user_id, date),

                        FOREIGN KEY(user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE

                    )
                    """)
    
#users
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users(

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        google_id TEXT UNIQUE,

                        name TEXT,

                        email TEXT UNIQUE,
                   
                        password_hash TEXT,

                        picture TEXT,

                        phone TEXT,

                        emergency_contact TEXT,

                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

                    )
                """)
    
    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_tables()

    print("Database Created Successfully!")

#2
from datetime import date

# chat
def save_chat(user_id, role, message):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO chat_history(
            user_id,
            role,
            message
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        role,
        message
    ))

    conn.commit()
    conn.close()

# moods
def save_mood(user_id, mood):

    conn = get_connection()
    cur = conn.cursor()

    today = date.today().isoformat()

    cur.execute("""
        INSERT INTO mood_history(
            user_id,
            date,
            mood
        )
        VALUES (?, ?, ?)

        ON CONFLICT(user_id, date)

        DO UPDATE SET
            mood = excluded.mood
    """, (
        user_id,
        today,
        mood
    ))

    conn.commit()
    conn.close()

def get_all_moods(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            date,
            mood
        FROM mood_history
        WHERE user_id = ?
        ORDER BY date
    """, (user_id,))

    rows = cur.fetchall()

    conn.close()

    return rows

# JOURNAL
def save_journal(
    user_id,
    mood,
    prompt,
    journal
):

    conn = get_connection()
    cur = conn.cursor()

    today = date.today().isoformat()

    cur.execute("""
        INSERT INTO journal(
            user_id,
            date,
            mood,
            prompt,
            journal
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(user_id, date)

        DO UPDATE SET

            mood = excluded.mood,
            prompt = excluded.prompt,
            journal = excluded.journal
    """, (
        user_id,
        today,
        mood,
        prompt,
        journal
    ))

    conn.commit()
    conn.close()

def load_journal(user_id):

    conn = get_connection()
    cur = conn.cursor()

    today = date.today().isoformat()

    cur.execute("""
        SELECT journal
        FROM journal
        WHERE
            user_id = ?
            AND date = ?
    """, (
        user_id,
        today
    ))

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return ""

# USERS
def get_user(email):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cur.fetchone()

    conn.close()

    return user

def create_user(
        
    google_id,
    name,
    email,
    picture,
    phone=None,
    emergency_contact=None
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO users(
            google_id,
            name,
            email,
            picture,
            phone,
            emergency_contact
        )
        VALUES(?,?,?,?,?,?)
    """,
    (
        google_id,
        name,
        email,
        picture,
        phone,
        emergency_contact
    ))

    conn.commit()
    conn.close()

def update_user_contact(
    user_id,
    phone,
    emergency_contact
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET
            phone = ?,
            emergency_contact = ?
        WHERE id = ?
    """, (
        phone,
        emergency_contact,
        user_id
    ))

    conn.commit()
    conn.close()

def get_user_by_id(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user

def get_mood_by_date(user_id, selected_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT mood
        FROM mood_history
        WHERE
            user_id = ?
            AND date = ?
    """, (
        user_id,
        selected_date
    ))

    row = cur.fetchone()

    conn.close()

    if row:
        return row["mood"]

    return None

def get_journal_by_date(user_id, selected_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT journal
        FROM journal
        WHERE
            user_id = ?
            AND date = ?
    """, (
        user_id,
        selected_date
    ))

    row = cur.fetchone()

    conn.close()

    if row:
        return row["journal"]

    return None

def get_chat_by_date(user_id, selected_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, message, timestamp
        FROM chat_history
        WHERE
            user_id = ?
            AND DATE(timestamp) = ?
        ORDER BY timestamp
    """, (
        user_id,
        selected_date
    ))

    rows = cur.fetchall()

    conn.close()

    return rows

def load_chat_history(user_id, selected_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, message
        FROM chat_history
        WHERE
            user_id = ?
            AND DATE(timestamp) = ?
        ORDER BY timestamp
    """, (
        user_id,
        selected_date
    ))

    rows = cur.fetchall()

    conn.close()

    return rows

from langchain_core.messages import HumanMessage, AIMessage


from datetime import date
from langchain_core.messages import HumanMessage, AIMessage


def get_recent_messages(user_id):

    today = date.today().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, message
        FROM chat_history
        WHERE
            user_id = ?
            AND DATE(timestamp) = ?
        ORDER BY timestamp
    """, (
        user_id,
        today
    ))

    rows = cur.fetchall()

    conn.close()

    messages = []

    for row in rows:

        if row["role"] == "user":
            messages.append(
                HumanMessage(content=row["message"])
            )

        else:
            messages.append(
                AIMessage(content=row["message"])
            )

    return messages

def clear_chat_history(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM chat_history
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

# Create tables automatically when the module is imported
create_tables()
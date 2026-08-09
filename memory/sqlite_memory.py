import sqlite3
from datetime import datetime

DB_PATH = "data/financial_assistant.db"

def initialize_database():
    import os
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                message TEXT,
                created_at TEXT
            )
        """)

def save_message(user_id, role, message):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO conversations(user_id,role,message,created_at) VALUES(?,?,?,?)",
            (user_id, role, message, datetime.now().isoformat()),
        )

def get_history(user_id, limit=30):
    with sqlite3.connect(DB_PATH) as con:
        rows = con.execute(
            "SELECT role,message,created_at FROM conversations "
            "WHERE user_id=? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return list(reversed(rows))

def clear_history(user_id):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DELETE FROM conversations WHERE user_id=?", (user_id,))

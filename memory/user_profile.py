import sqlite3

DB_PATH = "data/financial_assistant.db"

def initialize_profile_table():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS investor_profiles (
                user_id TEXT PRIMARY KEY,
                client_name TEXT,
                risk_profile TEXT,
                preferred_industries TEXT,
                investment_interests TEXT,
                frequent_companies TEXT
            )
        """)

def save_profile(user_id, client_name, risk_profile, preferred_industries,
                 investment_interests, frequent_companies):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            INSERT OR REPLACE INTO investor_profiles
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id, client_name, risk_profile, preferred_industries,
            investment_interests, frequent_companies
        ))

def get_profile(user_id):
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute(
            "SELECT * FROM investor_profiles WHERE user_id=?", (user_id,)
        ).fetchone()
    if not row:
        return None
    return {
        "user_id": row[0],
        "client_name": row[1],
        "risk_profile": row[2],
        "preferred_industries": row[3],
        "investment_interests": row[4],
        "frequent_companies": row[5],
    }

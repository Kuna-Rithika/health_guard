import sqlite3
from pathlib import Path

DB_NAME = "healthguard.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================================
    # USERS
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==================================================
    # SYMPTOM HISTORY
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptom_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        symptoms TEXT,
        risk_level TEXT,
        risk_score INTEGER,
        ai_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # ==================================================
    # HEALTH REPORTS
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        report_type TEXT,
        report_content TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # ==================================================
    # PREDICTIONS
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        prediction TEXT,
        confidence REAL,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# ======================================================
# DEMO USERS
# ======================================================

def seed_demo_users():

    conn = get_connection()
    cursor = conn.cursor()

    demo_users = [

        (
            "John Smith",
            "john@gmail.com",
            "john123",
            52,
            "Male"
        ),

        (
            "Sarah Johnson",
            "sarah@gmail.com",
            "sarah123",
            28,
            "Female"
        ),

        (
            "Mike Brown",
            "mike@gmail.com",
            "mike123",
            35,
            "Male"
        ),

        (
            "Emma Wilson",
            "emma@gmail.com",
            "emma123",
            40,
            "Female"
        ),

        (
            "David Lee",
            "david@gmail.com",
            "david123",
            65,
            "Male"
        ),

        (
            "Olivia Martin",
            "olivia@gmail.com",
            "olivia123",
            58,
            "Female"
        )

    ]

    for user in demo_users:

        cursor.execute("""
        INSERT OR IGNORE INTO users(
            full_name,
            email,
            password,
            age,
            gender
        )
        VALUES (?, ?, ?, ?, ?)
        """, user)

    conn.commit()
    conn.close()


# ======================================================
# DATABASE INITIALIZATION
# ======================================================

def initialize_database():

    create_tables()
    seed_demo_users()

    print("HealthGuard Database Ready")


if __name__ == "__main__":
    initialize_database()
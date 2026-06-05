import psycopg2
import os

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_9VTs7DPxtZIA@ep-delicate-lake-apgg4j7n-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

def get_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptom_history(
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        symptoms TEXT,
        risk_level TEXT,
        risk_score INTEGER,
        ai_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_reports(
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        report_type TEXT,
        report_content TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        prediction TEXT,
        confidence REAL,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

def seed_demo_users():
    conn = get_connection()
    cursor = conn.cursor()

    demo_users = [
        ("John Smith", "john@gmail.com", "john123", 52, "Male"),
        ("Sarah Johnson", "sarah@gmail.com", "sarah123", 28, "Female"),
        ("Mike Brown", "mike@gmail.com", "mike123", 35, "Male"),
        ("Emma Wilson", "emma@gmail.com", "emma123", 40, "Female"),
        ("David Lee", "david@gmail.com", "david123", 65, "Male"),
        ("Olivia Martin", "olivia@gmail.com", "olivia123", 58, "Female")
    ]

    for user in demo_users:
        cursor.execute("""
        INSERT INTO users(full_name, email, password, age, gender)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING
        """, user)

    conn.commit()
    conn.close()

def initialize_database():
    create_tables()
    seed_demo_users()
    print("HealthGuard Database Ready")

if __name__ == "__main__":
    initialize_database()
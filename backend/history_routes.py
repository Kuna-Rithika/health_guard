from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_NAME = "healthguard.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/history/{user_id}")
def get_user_history(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(
        """
        SELECT *
        FROM symptom_history
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({
            "id": row["id"],
            "symptoms": row["symptoms"],
            "risk_level": row["risk_level"],
            "risk_score": row["risk_score"],
            "summary": row["ai_summary"],
            "date": row["created_at"]
        })

    return history
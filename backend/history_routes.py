from fastapi import APIRouter
from .database import get_connection

router = APIRouter()

@router.get("/history/{user_id}")
def get_user_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, symptoms, risk_level, risk_score, ai_summary, created_at
        FROM symptom_history
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "symptoms": row[1],
            "risk_level": row[2],
            "risk_score": row[3],
            "summary": row[4],
            "date": row[5]
        })

    return history
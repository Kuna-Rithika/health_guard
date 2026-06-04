from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .auth import router as auth_router
from .health_routes import router as health_router
from .history_routes import router as history_router
from .database import get_connection
from .report_generator import generate_report_pdf
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO

app = FastAPI(
    title="HealthGuard API",
    description="Multi-Agent AI Health Assistant",
    version="1.0.0"
)

# ✅ CORS - must be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(history_router)

# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {
        "project": "HealthGuard",
        "status": "running",
        "version": "1.0.0",
        "time": datetime.now()
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "HealthGuard Backend Running"
    }


# =====================================================
# USERS
# =====================================================

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(
        """
        SELECT id, full_name, email, age, gender
        FROM users
        """
    ).fetchall()

    conn.close()

    users = [
        {
            "id": row["id"],
            "name": row["full_name"],
            "email": row["email"],
            "age": row["age"],
            "gender": row["gender"]
        }
        for row in rows
    ]

    return {
        "count": len(users),
        "users": users
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    user_row = cursor.execute(
        """
        SELECT id, full_name, email, age, gender
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    if not user_row:
        conn.close()
        return {
            "error": "User not found"
        }

    latest_history = cursor.execute(
        """
        SELECT risk_level, risk_score, ai_summary, created_at
        FROM symptom_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    return {
        "id": user_row["id"],
        "name": user_row["full_name"],
        "email": user_row["email"],
        "age": user_row["age"],
        "gender": user_row["gender"],
        "risk": latest_history["risk_level"] if latest_history else "UNKNOWN",
        "risk_score": latest_history["risk_score"] if latest_history else None,
        "condition": latest_history["ai_summary"] if latest_history else "No condition history"
    }


@app.get("/report/{user_id}")
def download_report(user_id: int):
    pdf_bytes = generate_report_pdf(user_id)
    return StreamingResponse(BytesIO(pdf_bytes), media_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename=HealthGuard_Report_{user_id}.pdf'
    })

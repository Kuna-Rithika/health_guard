from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .auth import router as auth_router
from .health_routes import router as health_router
from .history_routes import router as history_router
from .database import get_connection, initialize_database
from .report_generator import generate_report_pdf
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI(
    title="HealthGuard API",
    description="Multi-Agent AI Health Assistant",
    version="1.0.0"
)

# CORS first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    initialize_database()

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

    cursor.execute("""
        SELECT id, full_name, email, age, gender
        FROM users
    """)
    rows = cursor.fetchall()
    conn.close()

    users = [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3],
            "gender": row[4]
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

    cursor.execute("""
        SELECT id, full_name, email, age, gender
        FROM users
        WHERE id = %s
    """, (user_id,))
    user_row = cursor.fetchone()

    if not user_row:
        conn.close()
        return {"error": "User not found"}

    cursor.execute("""
        SELECT risk_level, risk_score, ai_summary, created_at
        FROM symptom_history
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))
    latest_history = cursor.fetchone()

    conn.close()

    return {
        "id": user_row[0],
        "name": user_row[1],
        "email": user_row[2],
        "age": user_row[3],
        "gender": user_row[4],
        "risk": latest_history[0] if latest_history else "UNKNOWN",
        "risk_score": latest_history[1] if latest_history else None,
        "condition": latest_history[2] if latest_history else "No condition history"
    }

@app.get("/report/{user_id}")
def download_report(user_id: int):
    pdf_bytes = generate_report_pdf(user_id)
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=HealthGuard_Report_{user_id}.pdf'
        }
    )
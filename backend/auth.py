from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .database import get_connection

router = APIRouter()

SECRET_KEY = "healthguard_secret_key_2026"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# =====================================================
# MODELS
# =====================================================

class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str
    age: int = None
    gender: str = None

class LoginRequest(BaseModel):
    email: str
    password: str

# =====================================================
# PASSWORD
# =====================================================

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# =====================================================
# JWT
# =====================================================

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# =====================================================
# SIGNUP
# =====================================================

@router.post("/signup")
def signup(user: SignupRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (user.email,)
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    cursor.execute(
        """
        INSERT INTO users(full_name, email, password, age, gender)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (user.full_name, user.email, hashed_password, user.age, user.gender)
    )

    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    token = create_token(user_id)

    return {
        "success": True,
        "message": "Account created successfully",
        "token": token,
        "user_id": user_id
    }

# =====================================================
# LOGIN
# =====================================================

@router.post("/login")
def login(data: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (data.email,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, user[3]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(user[0])

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
    }
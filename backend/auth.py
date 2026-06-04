from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import sqlite3

router = APIRouter()

SECRET_KEY = "healthguard_secret_key_2026"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

DB_NAME = "healthguard.db"


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
# DATABASE
# =====================================================

def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


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

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =====================================================
# SIGNUP
# =====================================================

@router.post("/signup")
def signup(user: SignupRequest):

    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (user.email,)
    ).fetchone()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    cursor.execute(
        """
        INSERT INTO users(
            full_name,
            email,
            password,
            age,
            gender
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user.full_name,
            user.email,
            hashed_password,
            user.age,
            user.gender
        )
    )

    conn.commit()

    user_id = cursor.lastrowid

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

    user = cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (data.email,)
    ).fetchone()

    conn.close()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(
        user["id"]
    )

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"]
        }
    }
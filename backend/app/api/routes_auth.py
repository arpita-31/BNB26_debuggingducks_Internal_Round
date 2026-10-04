"""
Authentication Routes for ReLearn
Handles user registration, login with JWT tokens, and identity retrieval.
Supports 'student' and 'teacher' roles.
"""
import uuid
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.database.db import get_db
from app.database.models import DBUser
from app.schemas.api_models import UserRegisterRequest, UserLoginRequest
from app.utils.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register")
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """Registers a new user (student or teacher) and returns access token."""
    existing = db.query(DBUser).filter_by(email=payload.email.strip().lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user_id = f"user_{uuid.uuid4().hex[:8]}"
    username = payload.email.split("@")[0]

    new_user = DBUser(
        id=user_id,
        email=payload.email.strip().lower(),
        username=username,
        full_name=payload.full_name.strip(),
        role=payload.role.strip().lower() if payload.role in ["student", "teacher"] else "student",
        hashed_password=hash_password(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({
        "sub": new_user.id,
        "email": new_user.email,
        "role": new_user.role,
        "full_name": new_user.full_name
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role
        }
    }

@router.post("/login")
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticates credentials and returns JWT token with user profile."""
    user = db.query(DBUser).filter_by(email=payload.email.strip().lower()).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "full_name": user.full_name
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name or user.username,
            "role": user.role or "student"
        }
    }

@router.get("/me")
def get_current_user_profile(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Retrieves current user identity from Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    user = db.query(DBUser).filter_by(id=payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name or user.username,
        "role": user.role or "student"
    }

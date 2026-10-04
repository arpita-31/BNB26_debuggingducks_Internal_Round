"""
Authentication and Cryptographic Utilities for ReLearn
Uses PBKDF2-HMAC-SHA256 with cryptographically random salt and PyJWT.
"""
import os
import secrets
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

JWT_SECRET = os.getenv("JWT_SECRET", "relearn-super-secret-key-2026-production-ready")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def hash_password(password: str) -> str:
    """Hashes a password with a unique 16-byte random salt using PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}:{key.hex()}"

def verify_password(password: str, hashed_value: str) -> bool:
    """Verifies a plain password against the stored salt:hash string."""
    try:
        salt, stored_hash = hashed_value.split(":")
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return computed_key.hex() == stored_hash
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generates a signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        return None

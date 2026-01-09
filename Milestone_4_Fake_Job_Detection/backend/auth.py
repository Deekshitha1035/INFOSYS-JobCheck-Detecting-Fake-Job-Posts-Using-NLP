# auth.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

# =======================
# Load environment variables
# =======================
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# =======================
# Password Hashing
# =======================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    Only first 72 characters are used (bcrypt limitation).
    """
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    """
    return pwd_context.verify(plain_password[:72], hashed_password)

# =======================
# JWT Token Functions
# =======================
def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: dictionary containing user info (e.g., {"username": "admin", "role": "admin"})
        expires_delta: optional timedelta to override default expiry

    Returns:
        JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token and return the payload if valid.

    Returns:
        dict payload if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# =======================
# FastAPI Dependency
# =======================
from fastapi import Header, HTTPException

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency to extract the current user from the Authorization header.

    Accepts:
        - "Bearer <token>"
        - "<token>" (just token)

    Raises:
        HTTPException 401 if missing or invalid token.

    Returns:
        payload dictionary containing user info
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    parts = authorization.split()
    if len(parts) == 1:
        token = parts[0]  # token only
    elif len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]  # "Bearer <token>"
    else:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user

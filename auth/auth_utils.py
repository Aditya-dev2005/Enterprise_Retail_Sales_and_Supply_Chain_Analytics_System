from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from configs.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRY_MINUTES
from database.database_connection import sessionLocal
from models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def hash_password(plain_password: str) -> str:
    # bcrypt has a 72-byte input limit - truncate defensively.
    password_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRY_MINUTES)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    A FastAPI dependency - add `current_user: dict = Depends(get_current_user)`
    as a parameter to any route to require a valid JWT token before it runs.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise credentials_exception

    session = sessionLocal()
    try:
        user = session.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return {"username": user.username, "role": user.role}
    finally:
        session.close()

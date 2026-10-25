from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from auth.auth_utils import hash_password, verify_password, create_access_token, get_current_user
from database.database_connection import sessionLocal
from models.models import User
from logger_config import logger

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", description="'user' or 'admin'")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest):
    session = sessionLocal()
    try:
        existing = session.query(User).filter(User.username == request.username).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username already exists")

        new_user = User(
            username=request.username,
            hashed_password=hash_password(request.password),
            role=request.role,
            created_at=datetime.utcnow(),
        )
        session.add(new_user)
        session.commit()
        logger.info(f"New user registered: {request.username}")

        token = create_access_token(username=new_user.username, role=new_user.role)
        return TokenResponse(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.exception(f"Registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")
    finally:
        session.close()


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    session = sessionLocal()
    try:
        user = session.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        logger.info(f"User logged in: {user.username}")
        token = create_access_token(username=user.username, role=user.role)
        return TokenResponse(access_token=token)
    finally:
        session.close()


@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user

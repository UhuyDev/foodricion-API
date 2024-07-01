import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.Engine import get_db
from database.dtos import UserCreateRequest, UserCreateResponse
from models import User, Token
from utils.Security import create_access_token, create_refresh_token, authenticate_user, verify_refresh_token, \
    pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES
import time

AuthRouter = APIRouter()


@AuthRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(
        user_id=str(uuid.uuid4()),
        email=user_data.email,
        password_hash=hashed_password,
        fullname=user_data.fullname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "code": status.HTTP_201_CREATED,
        "message": "Registration success",
        "data": UserCreateResponse(fullname=db_user.fullname, email=db_user.email)
    }


@AuthRouter.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db.query(Token).filter(Token.user_id == user.user_id).delete()
    db.commit()
    tdelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + tdelta
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=tdelta
    )
    refresh_token = create_refresh_token(user.user_id, db)
    return {
        "code": status.HTTP_200_OK,
        "message": "Login success",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires": int(expire.timestamp())
    }


@AuthRouter.post("/refresh-token")
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    db_token = verify_refresh_token(refresh_token, db)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tdelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + tdelta
    access_token = create_access_token(
        data={"sub": str(db_token.user_id)}, expires_delta=tdelta
    )
    return {
        "code": status.HTTP_200_OK,
        "message": "Token refresh success",
        "access_token": access_token,
        "expires": int(expire.timestamp())
    }

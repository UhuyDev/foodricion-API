import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.Engine import get_db
from database.dtos import UserCreateRequest, UserCreateResponse, LoginRequest, APIResponse
from models import User, Token
from utils.Security import create_access_token, create_refresh_token, authenticate_user, verify_refresh_token, \
    pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES

AuthRouter = APIRouter()


# Endpoint to register a new user
@AuthRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
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

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Registration success",
        data=UserCreateResponse(fullname=db_user.fullname, email=db_user.email)
    )


# Endpoint to log in and get access token
@AuthRouter.post("/login")
async def login_for_access_token(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(login_data.email, login_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db.query(Token).filter(Token.user_id == user.user_id).delete()
    db.commit()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expired_at = datetime.now(timezone.utc) + access_token_expires
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(user.user_id, db)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Login success",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expired_at": int(access_token_expired_at.timestamp())
        }
    )


# Endpoint to refresh access token using a refresh token
@AuthRouter.post("/refresh-token")
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    db_token = verify_refresh_token(refresh_token, db)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expired_at = datetime.now(timezone.utc) + access_token_expires
    access_token = create_access_token(
        data={"sub": str(db_token.user_id)}, expires_delta=access_token_expires
    )

    # Create a new refresh token
    new_refresh_token = create_refresh_token(db_token.user_id, db)

    # Delete the old refresh token from the database
    db.query(Token).filter(Token.token == refresh_token).delete()
    db.commit()

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Token refresh success",
        data={
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "expired_at": int(access_token_expired_at.timestamp())
        }
    )

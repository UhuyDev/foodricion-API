import os
import uvicorn
from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
import models
from database import engine, Sessionlocal

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class UserInResponse(BaseModel):
    fullname: str
    email: str

    class Config:
        orm_mode = True


class NutritionBase(BaseModel):
    food_id: int
    food_image: str
    food_name: str
    food_type: str
    food_calories: float


class ChatbotHistoryCreate(BaseModel):
    message: str
    response: str


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def get_user(email: str):
    db = Sessionlocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    db.close()
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/register", response_model=UserInResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user_data.password)
    db_user = models.User(email=user_data.email, password_hash=hashed_password, fullname=user_data.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInResponse(fullname=db_user.fullname, email=db_user.email)


@app.get("/", status_code=status.HTTP_200_OK)
def github():
    return RedirectResponse("https://github.com/UhuyDev")


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserInResponse)
async def read_current_user(current_user: models.User = Depends(get_current_user)):
    return UserInResponse(fullname=current_user.fullname, email=current_user.email)


@app.get("/nutrition", status_code=status.HTTP_200_OK)
async def read_nutrition_all(db: db_dependency):
    nutrition_all = db.query(models.Nutrition).all()
    if not nutrition_all:
        raise HTTPException(status_code=404, detail='Nutrition data not found')
    return nutrition_all


@app.get("/nutrition/{food_name}", status_code=status.HTTP_200_OK)
async def read_nutrition_name(food_name: str, db: db_dependency):
    nutrition_name = db.query(models.Nutrition).filter(models.Nutrition.food_name == food_name).first()
    if not nutrition_name:
        raise HTTPException(status_code=404, detail='Nutrition data not found')
    return nutrition_name


@app.get("/chatbot-history", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def read_chatbot_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_id = current_user.user_id

    stmt = (db.query(models.ChatbotConversation)
            .filter(models.ChatbotConversation.user_id == user_id)
            .order_by(models.ChatbotConversation.timestamp.desc()))
    chatbot_history = stmt.all()

    if not chatbot_history:
        raise HTTPException(status_code=404, detail='Chatbot history not found for this user')

    return chatbot_history


@app.post("/chatbot-history", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_chatbot_history(
    chatbot_data: ChatbotHistoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Create a new chatbot history entry with the current user's user_id
    db_chatbot = models.ChatbotConversation(
        message=chatbot_data.message,
        response=chatbot_data.response,
        user_id=current_user.user_id  # Use the user_id from the current_user object
    )
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
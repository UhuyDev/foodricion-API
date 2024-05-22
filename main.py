import os
import uuid
from datetime import datetime, timedelta, timezone
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, Sessionlocal

# Load environment variables from a .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password context with bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define OAuth2 scheme for obtaining tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Define Pydantic models for user creation and response
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class UserInResponse(BaseModel):
    fullname: str
    email: str

    class Config:
        from_attributes = True


# Define Pydantic model for chatbot history creation
class ChatbotHistoryCreate(BaseModel):
    message: str
    response: str


class BookmarkCreate(BaseModel):
    food_id: int


# Function to create an access token for a user
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify a plain password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to authenticate a user by email and password
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None


# Dependency to get a database session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# Dependency to get the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


# Initialize FastAPI application
app = FastAPI()

# Create all database tables
models.Base.metadata.create_all(bind=engine)


# Root endpoint to check if the API is working
@app.get("/", status_code=status.HTTP_200_OK)
def welcome():
    return "foodricion-api is working"


# Endpoint to register a new user
@app.post("/register", response_model=UserInResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user_data.password)
    db_user = models.User(
        user_id=str(uuid.uuid4()),
        email=user_data.email,
        password_hash=hashed_password,
        fullname=user_data.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInResponse(fullname=db_user.fullname, email=db_user.email)


# Endpoint to obtain an access token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint to get the current authenticated user's information
@app.get("/me", response_model=UserInResponse)
async def read_current_user(current_user: models.User = Depends(get_current_user)):
    return UserInResponse(fullname=current_user.fullname, email=current_user.email)


# Endpoint to get all nutrition data
@app.get("/nutrition", status_code=status.HTTP_200_OK)
async def read_nutrition_all(db: Session = Depends(get_db)):
    nutrition_all = db.query(models.Nutrition).all()
    if not nutrition_all:
        raise HTTPException(status_code=404, detail='Nutrition data not found')
    return nutrition_all


# Endpoint to get nutrition data by food name
@app.get("/nutrition/{food_name}", status_code=status.HTTP_200_OK)
async def read_nutrition_name(food_name: str, db: Session = Depends(get_db)):
    nutrition_name = db.query(models.Nutrition).filter(models.Nutrition.food_name == food_name).first()
    if not nutrition_name:
        raise HTTPException(status_code=404, detail='Nutrition data not found')
    return nutrition_name


# Endpoint to get chatbot history for the current user
@app.get("/chatbot-history", status_code=status.HTTP_200_OK)
async def read_chatbot_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatbot_history = db.query(models.ChatbotConversation).filter(
        models.ChatbotConversation.user_id == current_user.user_id).order_by(
        models.ChatbotConversation.timestamp.desc()).all()
    if not chatbot_history:
        raise HTTPException(status_code=404, detail='Chatbot history not found for this user')
    return chatbot_history


# Endpoint to create a new chatbot history entry
@app.post("/chatbot-history", status_code=status.HTTP_201_CREATED)
async def create_chatbot_history(chatbot_data: ChatbotHistoryCreate,
                                 current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_chatbot = models.ChatbotConversation(
        message=chatbot_data.message,
        response=chatbot_data.response,
        user_id=current_user.user_id
    )
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot


# Endpoint to get all bookmarks for the current user
@app.get("/bookmarks", status_code=status.HTTP_200_OK)
async def get_bookmarks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    bookmarks = db.query(models.BookmarkedNutrition).filter(
        models.BookmarkedNutrition.user_id == current_user.user_id).all()
    if not bookmarks:
        raise HTTPException(status_code=404, detail='Bookmarks not found for this user')
    return bookmarks


# Endpoint to create a new bookmark for the current user
@app.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def create_bookmark(bookmark_data: BookmarkCreate,
                          current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_bookmark = db.query(models.BookmarkedNutrition).filter(
        models.BookmarkedNutrition.user_id == current_user.user_id,
        models.BookmarkedNutrition.food_id == bookmark_data.food_id
    ).first()
    if existing_bookmark:
        raise HTTPException(status_code=400, detail='Bookmark already exists for this food item')

    db_bookmark = models.BookmarkedNutrition(
        user_id=current_user.user_id,
        food_id=bookmark_data.food_id
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, CHAR
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=False)
    registration_date = Column(DateTime, default=datetime.now(timezone.utc))


class Nutrition(Base):
    __tablename__ = 'nutrition_table'
    food_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    food_name = Column(String(255), nullable=False, index=True)
    food_image = Column(String(255))
    food_type = Column(String(255))
    food_calories = Column(Float)


class BookmarkedNutrition(Base):
    __tablename__ = 'nutrition_bookmark'
    bookmark_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), index=True)
    food_id = Column(Integer, ForeignKey("nutrition_table.food_id"), index=True)
    bookmark_date = Column(DateTime, default=datetime.now(timezone.utc))


class ChatbotConversation(Base):
    __tablename__ = 'chatbot_conversations'
    conversation_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), index=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String(255))
    response = Column(String(255))

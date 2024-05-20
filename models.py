from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

from database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    fullname = Column(String(255))
    registration_date = Column(DateTime, default=datetime.now(timezone.utc))


class Nutrition(Base):
    __tablename__ = 'nutrition_table'
    food_id = Column(Integer, primary_key=True, index=True)
    food_image = Column(String(255))
    food_name = Column(String(255))
    food_type = Column(String(255))
    food_calories = Column(Float)


class ScannedImage(Base):
    __tablename__ = 'scanned_images'
    image_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    image_path = Column(String(255))
    scan_date = Column(DateTime, default=datetime.now(timezone.utc))
    result = Column(String(255))


class ChatbotConversation(Base):
    __tablename__ = 'chatbot_conversations'
    conversation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String)
    response = Column(String)

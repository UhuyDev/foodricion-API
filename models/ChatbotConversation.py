from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR

from .Base import Base


class ChatbotConversation(Base):
    __tablename__ = 'chatbot_conversations'
    conversation_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), index=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    message = Column(String(255))
    response = Column(String(255))
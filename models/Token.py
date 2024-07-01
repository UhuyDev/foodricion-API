import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, CHAR
from .Base import Base
from .User import User


class Token(Base):
    __tablename__ = "tokens"
    token_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)

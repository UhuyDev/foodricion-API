import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, CHAR

from .Base import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=False)
    registration_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

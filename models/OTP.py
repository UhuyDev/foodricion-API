from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR
from .Base import Base


class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), nullable=False)
    otp_code = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expiry_at = Column(DateTime)

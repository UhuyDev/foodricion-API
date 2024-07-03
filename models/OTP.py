from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, CHAR
from .Base import Base
from .User import User

class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), nullable=False)
    otp_code = Column(String(6), nullable=False)
    created_at = Column(BigInteger, default=lambda: int(datetime.now(timezone.utc).timestamp()))
    expiry_at = Column(BigInteger)  # Store timestamps as BigInteger
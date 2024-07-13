from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, CHAR

from .Base import Base
from .User import User


class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), nullable=False)
    otp_code = Column(String(6), nullable=False)
    expires_at = Column(BigInteger)

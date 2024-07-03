import uuid
from sqlalchemy import Column, BigInteger, ForeignKey, CHAR, String
from .Base import Base
from .User import User


class Token(Base):
    __tablename__ = "tokens"
    token_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), nullable=False)
    token = Column(String(255), nullable=False)
    expires_at = Column(BigInteger)

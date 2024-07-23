from sqlalchemy import Column, Integer, ForeignKey, CHAR

from .Base import Base


class UserDetail(Base):
    __tablename__ = 'users_details'
    user_detail_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), index=True)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)

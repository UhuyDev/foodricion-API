from sqlalchemy import Column, Integer, String
from .Base import Base


class Food(Base):
    __tablename__ = 'food'
    food_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    food_name = Column(String(255), nullable=False, unique=True, index=True)
    food_image = Column(String(255))
    food_type = Column(String(255))

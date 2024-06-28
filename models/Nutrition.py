from sqlalchemy import Column, Integer, String, Float

from .Base import Base


class Nutrition(Base):
    __tablename__ = 'nutrition_table'
    food_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    food_name = Column(String(255), nullable=False, index=True)
    food_image = Column(String(255))
    food_type = Column(String(255))
    food_calories = Column(Float)

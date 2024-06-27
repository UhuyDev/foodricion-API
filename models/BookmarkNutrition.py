from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, CHAR
from .Base import Base

class BookmarkNutrition(Base):
    __tablename__ = 'nutrition_bookmark'
    bookmark_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), index=True)
    food_id = Column(Integer, ForeignKey("nutrition_table.food_id"), index=True)
    bookmark_date = Column(DateTime, default=datetime.now(timezone.utc))
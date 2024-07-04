from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, ForeignKey, CHAR

from .Base import Base


class FoodBookmark(Base):
    __tablename__ = 'food_bookmark'
    bookmark_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), index=True)
    food_id = Column(Integer, ForeignKey("food.food_id"), index=True)
    bookmark_date = Column(DateTime, default=datetime.now(timezone.utc))

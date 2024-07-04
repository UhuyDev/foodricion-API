from sqlalchemy import Column, Integer, Float, ForeignKey, CHAR

from .Base import Base


class NutritionDetails(Base):
    __tablename__ = 'nutrition_details'
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    food_id = Column(Integer, ForeignKey('food.food_id'), nullable=False)
    energy = Column(Float)
    total_fat = Column(Float)
    vitamin_A = Column(Float)
    vitamin_B1 = Column(Float)
    vitamin_B2 = Column(Float)
    vitamin_B3 = Column(Float)
    vitamin_C = Column(Float)
    total_carbohydrate = Column(Float)
    protein = Column(Float)
    dietary_fiber = Column(Float)
    calcium = Column(Float)
    phosphorus = Column(Float)
    sodium = Column(Float)
    potassium = Column(Float)
    copper = Column(Float)
    iron = Column(Float)
    zinc = Column(Float)
    b_carotene = Column(Float)
    total_carotene = Column(Float)
    water = Column(Float)
    ash = Column(Float)

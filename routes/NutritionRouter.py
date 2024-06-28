from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from models import Nutrition

NutritionRouter = APIRouter()


@NutritionRouter.get("/nutrition", status_code=status.HTTP_200_OK)
async def read_nutrition_all(db: Session = Depends(get_db)):
    nutrition_all = db.query(Nutrition).all()
    if not nutrition_all:
        raise HTTPException(status_code=404, detail='Nutrition data not found')
    return nutrition_all


@NutritionRouter.get("/nutrition/{food_name}", status_code=status.HTTP_200_OK)
async def read_nutrition_name(food_name: str, db: Session = Depends(get_db)):
    nutrition_name = db.query(Nutrition).filter(Nutrition.food_name == food_name).first()
    if not nutrition_name:
        raise HTTPException(status_code=404, detail='Nutrition data not found')
    return nutrition_name

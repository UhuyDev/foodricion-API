from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database.Engine import get_db
from models import Food, Nutrition
from database.dtos import APIResponse

NutritionRouter = APIRouter()


# Endpoint to retrieve all food data with energy (calories) from nutrition table
@NutritionRouter.get("/foods", status_code=status.HTTP_200_OK)
async def read_food_all(db: Session = Depends(get_db)):
    food_all = (
        db.query(Food, Nutrition.energy)
        .join(Nutrition, Food.food_id == Nutrition.food_id)
        .all()
    )

    data = []
    for food, energy in food_all:
        data.append({
            "food_id": food.food_id,
            "food_name": food.food_name,
            "food_image": food.food_image,
            "food_type": food.food_type,
            "food_calories": energy
        })

    return APIResponse(
        code=status.HTTP_200_OK,
        message="All food data retrieved successfully",
        data=data
    )


# Endpoint to retrieve nutrition details by food name
@NutritionRouter.get("/foods/nutrition", status_code=status.HTTP_200_OK)
async def get_nutrition_by_name(food_name: str, db: Session = Depends(get_db)):
    food_with_nutrition = (
        db.query(Food, Nutrition)
        .join(Nutrition, Food.food_id == Nutrition.food_id)
        .filter(Food.food_name.contains(food_name))
        .first()
    )
    # Check if the food item with nutrition exists in the database
    if not food_with_nutrition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food or nutrition details not found")

    food, nutrition_details = food_with_nutrition

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Nutrition details retrieved successfully",
        data={
            "food_id": food.food_id,
            "food_name": food.food_name,
            "food_image": food.food_image,
            "food_type": food.food_type,
            "nutrition_details": {
                "energy": nutrition_details.energy,
                "total_fat": nutrition_details.total_fat,
                "saturated_fat": nutrition_details.saturated_fat,
                "polyunsaturated_fat": nutrition_details.polyunsaturated_fat,
                "cholesterol": nutrition_details.cholesterol,
                "sugar": nutrition_details.sugar,
                "vitamin_A": nutrition_details.vitamin_A,
                "vitamin_B1": nutrition_details.vitamin_B1,
                "vitamin_B2": nutrition_details.vitamin_B2,
                "vitamin_B3": nutrition_details.vitamin_B3,
                "vitamin_B6": nutrition_details.vitamin_B6,
                "vitamin_B9": nutrition_details.vitamin_B9,
                "vitamin_C": nutrition_details.vitamin_C,
                "vitamin_E": nutrition_details.vitamin_E,
                "total_carbohydrate": nutrition_details.total_carbohydrate,
                "protein": nutrition_details.protein,
                "dietary_fiber": nutrition_details.dietary_fiber,
                "calcium": nutrition_details.calcium,
                "phosphorus": nutrition_details.phosphorus,
                "magnesium": nutrition_details.magnesium,
                "sodium": nutrition_details.sodium,
                "potassium": nutrition_details.potassium,
                "copper": nutrition_details.copper,
                "iron": nutrition_details.iron,
                "zinc": nutrition_details.zinc,
                "b_carotene": nutrition_details.b_carotene,
                "total_carotene": nutrition_details.total_carotene,
                "water": nutrition_details.water,
                "ash": nutrition_details.ash
            }
        }
    )

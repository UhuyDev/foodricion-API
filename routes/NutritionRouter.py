from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from models import Food, NutritionDetails
from database.dtos import APIResponse

NutritionRouter = APIRouter()


@NutritionRouter.get("/food", status_code=status.HTTP_200_OK)
async def read_food_all(db: Session = Depends(get_db)):
    """Get all food data."""
    food_all = db.query(Food).all()
    return APIResponse(
        code=status.HTTP_200_OK,
        message="All food data retrieved successfully",
        data=[{
            "food_id": food.food_id,
            "food_name": food.food_name,
            "food_image": food.food_image,
            "food_type": food.food_type
        } for food in food_all]
    )


@NutritionRouter.get("/nutrition/{food_identifier}", status_code=status.HTTP_200_OK)
async def read_nutrition(food_identifier: str, db: Session = Depends(get_db)):
    """
    Get food and nutrition details by either food name or food_id.
    """
    try:
        # Check if identifier is food_id (integer)
        food_id = int(food_identifier)
        food = db.query(Food).filter(Food.food_id == food_id).first()
    except ValueError:
        # If not integer, assume its food_name
        food = db.query(Food).filter(Food.food_name == food_identifier).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    nutrition_details = (
        db.query(NutritionDetails).filter(NutritionDetails.food_id == food.food_id).first()
    )

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Food data retrieved successfully",
        data={
            "food_id": food.food_id,
            "food_name": food.food_name,
            "food_image": food.food_image,
            "food_type": food.food_type,
            "energy": nutrition_details.energy if nutrition_details else None,
            "total_fat": nutrition_details.total_fat if nutrition_details else None,
            "vitamin_A": nutrition_details.vitamin_A if nutrition_details else None,
            "vitamin_B1": nutrition_details.vitamin_B1 if nutrition_details else None,
            "vitamin_B2": nutrition_details.vitamin_B2 if nutrition_details else None,
            "vitamin_B3": nutrition_details.vitamin_B3 if nutrition_details else None,
            "vitamin_C": nutrition_details.vitamin_C if nutrition_details else None,
            "total_carbohydrate": nutrition_details.total_carbohydrate if nutrition_details else None,
            "protein": nutrition_details.protein if nutrition_details else None,
            "dietary_fiber": nutrition_details.dietary_fiber if nutrition_details else None,
            "calcium": nutrition_details.calcium if nutrition_details else None,
            "phosphorus": nutrition_details.phosphorus if nutrition_details else None,
            "sodium": nutrition_details.sodium if nutrition_details else None,
            "potassium": nutrition_details.potassium if nutrition_details else None,
            "copper": nutrition_details.copper if nutrition_details else None,
            "iron": nutrition_details.iron if nutrition_details else None,
            "zinc": nutrition_details.zinc if nutrition_details else None,
            "b_carotene": nutrition_details.b_carotene if nutrition_details else None,
            "total_carotene": nutrition_details.total_carotene if nutrition_details else None,
            "water": nutrition_details.water if nutrition_details else None,
            "ash": nutrition_details.ash if nutrition_details else None,
        }
    )

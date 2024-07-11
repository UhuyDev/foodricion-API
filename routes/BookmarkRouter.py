from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from database.dtos import BookmarkCreateRequest, APIResponse, BookmarkDeleteRequest
from models import FoodBookmark, User, Food, Nutrition
from utils.Security import get_current_user

BookmarkRouter = APIRouter()


@BookmarkRouter.get("/bookmarks", status_code=status.HTTP_200_OK)
async def get_bookmarks(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    bookmarks = (
        db.query(FoodBookmark, Food, Nutrition)
        .join(Food, Food.food_id == FoodBookmark.food_id)
        .join(Nutrition, Nutrition.food_id == Food.food_id)
        .filter(FoodBookmark.user_id == current_user.user_id)
        .all()
    )

    if not bookmarks:
        raise HTTPException(status_code=404, detail='Bookmarks not found for this user')

    bookmark_data = []
    for bookmark in bookmarks:
        if bookmark.Food and bookmark.Nutrition:
            bookmark_data.append({
                "bookmark": bookmark.FoodBookmark.bookmark_id,
                "food": bookmark.Food.food_name,
                "energy": bookmark.Nutrition.energy,
                "total_fat": bookmark.Nutrition.total_fat,
                "saturated_fat": bookmark.Nutrition.saturated_fat,
                "polyunsaturated_fat": bookmark.Nutrition.polyunsaturated_fat,
                "sugar": bookmark.Nutrition.sugar,
                "vitamin_A": bookmark.Nutrition.vitamin_A,
                "vitamin_B1": bookmark.Nutrition.vitamin_B1,
                "vitamin_B2": bookmark.Nutrition.vitamin_B2,
                "vitamin_B3": bookmark.Nutrition.vitamin_B3,
                "vitamin_C": bookmark.Nutrition.vitamin_C,
                "total_carbohydrate": bookmark.Nutrition.total_carbohydrate,
                "protein": bookmark.Nutrition.protein,
                "dietary_fiber": bookmark.Nutrition.dietary_fiber,
                "calcium": bookmark.Nutrition.calcium,
                "phosphorus": bookmark.Nutrition.phosphorus,
                "sodium": bookmark.Nutrition.sodium,
                "potassium": bookmark.Nutrition.potassium,
                "copper": bookmark.Nutrition.copper,
                "iron": bookmark.Nutrition.iron,
                "zinc": bookmark.Nutrition.zinc,
                "b_carotene": bookmark.Nutrition.b_carotene,
                "total_carotene": bookmark.Nutrition.total_carotene,
                "water": bookmark.Nutrition.water,
                "ash": bookmark.Nutrition.ash
            })

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Bookmarks retrieved successfully",
        data=bookmark_data
    )


@BookmarkRouter.post("/bookmarks/", status_code=status.HTTP_201_CREATED)
async def create_bookmark(
        bookmark_request: BookmarkCreateRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    food_item = db.query(Food).filter(Food.food_name == bookmark_request.food_name).first()

    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    db_bookmark = FoodBookmark(
        user_id=current_user.user_id,
        food_id=food_item.food_id
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)

    return APIResponse(
        code=status.HTTP_201_CREATED,
        message="Bookmark created successfully",
        data={
            "bookmark_id": db_bookmark.bookmark_id,
            "food_id": db_bookmark.food_id,
            "bookmark_date": db_bookmark.bookmark_date,
        }
    )


@BookmarkRouter.delete("/bookmarks/", status_code=status.HTTP_200_OK)
async def delete_bookmark(
        bookmark_delete_request: BookmarkDeleteRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    bookmark = db.query(FoodBookmark).filter(
        FoodBookmark.bookmark_id == bookmark_delete_request.bookmark_id,
        FoodBookmark.user_id == current_user.user_id
    ).first()

    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    db.delete(bookmark)
    db.commit()

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Bookmark deleted successfully",
    )

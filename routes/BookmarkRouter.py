# BookmarkRouter.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from database.dtos import BookmarkCreateRequest
from models import FoodBookmark, User, Food, NutritionDetails
from utils.Security import get_current_user

BookmarkRouter = APIRouter()


@BookmarkRouter.get("/bookmarks", status_code=status.HTTP_200_OK)
async def get_bookmarks(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    bookmarks = db.query(FoodBookmark).filter(FoodBookmark.user_id == current_user.user_id).all()

    if not bookmarks:
        raise HTTPException(status_code=404, detail='Bookmarks not found for this user')

    bookmark_data = []
    for bookmark in bookmarks:
        food = db.query(Food).filter(Food.food_id == bookmark.food_id).first()
        nutrition = db.query(NutritionDetails).filter(NutritionDetails.food_id == bookmark.food_id).first()
        bookmark_data.append({
            "bookmark": bookmark,
            "food": food,
            "nutrition": nutrition
        })

    return bookmark_data


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

    return {
        "bookmark_id": db_bookmark.bookmark_id,
        "food_id": db_bookmark.food_id,
        "bookmark_date": db_bookmark.bookmark_date,
    }

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database.Engine import get_db
from database.dtos import APIResponse
from models import FoodBookmark, User, Food, NutritionDetails
from utils.Security import get_current_user

BookmarkRouter = APIRouter()


@BookmarkRouter.get("/bookmarks", status_code=status.HTTP_200_OK)
async def get_bookmarks(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        include_nutrition: bool = Query(False, description="Include nutrition details (True/False)")
):
    bookmarks = db.query(FoodBookmark).filter(FoodBookmark.user_id == current_user.user_id).all()

    if not bookmarks:
        raise HTTPException(status_code=404, detail='Bookmarks not found for this user')

    if include_nutrition:
        # Fetch and join the related nutrition data for each bookmark
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
    else:
        # Fetch only the food data related to the bookmark
        bookmark_data = []
        for bookmark in bookmarks:
            food = db.query(Food).filter(Food.food_id == bookmark.food_id).first()
            bookmark_data.append({
                "bookmark": bookmark,
                "food": food
            })
        return bookmark_data


@BookmarkRouter.post("/bookmarks/{food_identifier}", status_code=status.HTTP_201_CREATED)
async def create_bookmark(
        food_identifier: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Initialize variables
    food_id = None
    food_name = None

    try:
        # Check if identifier is food_id (integer)
        food_id = int(food_identifier)
    except ValueError:
        # If not integer, assume its food_name
        food_name = food_identifier

    # Allow creating bookmarks by food_name or food_id (priority to food_id)
    if food_id:
        food_item = db.query(Food).filter(Food.food_id == food_id).first()
    elif food_name:
        food_item = db.query(Food).filter(Food.food_name == food_name).first()
    else:
        raise HTTPException(status_code=400, detail="Either food_id or food_name is required")

    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    # Check if the bookmark already exists for this user and food
    db.query(FoodBookmark).filter(
        FoodBookmark.user_id == current_user.user_id,
        FoodBookmark.food_id == food_item.food_id
    ).first()

    # Create the new bookmark
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

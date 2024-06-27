from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.dtos import BookmarkCreateRequest
from database.Engine import get_db
from models import BookmarkNutrition, User
from utils.Security import get_current_user

BookmarkRouter = APIRouter()

@BookmarkRouter.get("/bookmarks", status_code=status.HTTP_200_OK)
async def get_bookmarks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bookmarks = db.query(BookmarkNutrition).filter(BookmarkNutrition.user_id == current_user.user_id).all()
    if not bookmarks:
        raise HTTPException(status_code=404, detail='Bookmarks not found for this user')
    return bookmarks

@BookmarkRouter.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def create_bookmark(bookmark_data: BookmarkCreateRequest,
                          current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_bookmark = db.query(BookmarkNutrition).filter(
        BookmarkNutrition.user_id == current_user.user_id,
        BookmarkNutrition.food_id == bookmark_data.food_id
    ).first()
    if existing_bookmark:
        raise HTTPException(status_code=400, detail='Bookmark already exists for this food item')

    db_bookmark = BookmarkNutrition(
        user_id=current_user.user_id,
        food_id=bookmark_data.food_id
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

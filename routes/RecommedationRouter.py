from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database.Engine import get_db
from models import User
from database.dtos import APIResponse
from utils.Security import get_current_user
from utils.FoodRecommedation import recommend_daily_food

RecommendationRouter = APIRouter()


@RecommendationRouter.get("/recommend", status_code=status.HTTP_200_OK)
async def recommend_food(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = recommend_daily_food(current_user.user_id, db)
        if result["status"] == "success":
            return APIResponse(
                code=status.HTTP_200_OK,
                message=result["message"],
                data=result.get("data")
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

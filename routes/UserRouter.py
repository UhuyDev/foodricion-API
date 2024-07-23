from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.Engine import get_db
from database.dtos import ProfileUpdateRequest, PasswordChangeRequest, APIResponse, \
    UserMetricsUpdateRequest
from models import User, UserMetrics
from utils.Security import get_current_user, verify_password, pwd_context

# Initialize the APIRouter for user-related operations
UserRouter = APIRouter()


# Route to get the current user's details
@UserRouter.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_metrics = db.query(UserMetrics).filter(UserMetrics.user_id == current_user.user_id).first()

    if user_metrics:
        data = {
            "fullname": current_user.fullname,
            "email": current_user.email,
            "age": user_metrics.age,
            "height": user_metrics.height,
            "weight": user_metrics.weight
        }
    else:
        data = {
            "fullname": current_user.fullname,
            "email": current_user.email
        }

    return APIResponse(
        code=status.HTTP_200_OK,
        message="User details retrieved successfully",
        data=data
    )


# Route to update the current user's metrics (UserDetail)
@UserRouter.post("/me/update-metrics", status_code=status.HTTP_200_OK)
async def update_metrics(user_metrics_update_request: UserMetricsUpdateRequest,
                         current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_metrics = db.query(UserMetrics).filter(UserMetrics.user_id == current_user.user_id).first()
    if not user_metrics:
        user_metrics = UserMetrics(user_id=current_user.user_id)
        db.add(user_metrics)

    user_metrics.age = user_metrics_update_request.age
    user_metrics.height = user_metrics_update_request.height
    user_metrics.weight = user_metrics_update_request.weight
    db.commit()
    db.refresh(user_metrics)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Metrics updated successfully",
        data={
            "age": user_metrics.age,
            "height": user_metrics.height,
            "weight": user_metrics.weight
        }
    )


# Route to update the current user's profile
@UserRouter.post("/me/update-profile", status_code=status.HTTP_200_OK)
async def update_profile(profile_update_request: ProfileUpdateRequest,
                         current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if another user already registers the new email
    if current_user.email != profile_update_request.email:
        existing_user = db.query(User).filter(User.email == profile_update_request.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Update the user's profile details
    current_user.fullname = profile_update_request.full_name
    current_user.email = profile_update_request.email
    db.commit()
    db.refresh(current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Profile updated successfully",
        data={
            "email": current_user.email,
            "fullname": current_user.fullname
        }
    )


# Route to change the current user's password
@UserRouter.post("/me/change-password", status_code=status.HTTP_200_OK)
async def change_password(password_change_request: PasswordChangeRequest,
                          current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verify the old password
    if not verify_password(password_change_request.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    # Hash the new password and update it in the database
    new_hashed_password = pwd_context.hash(password_change_request.new_password)
    current_user.password_hash = new_hashed_password
    db.commit()
    db.refresh(current_user)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Password changed successfully"
    )

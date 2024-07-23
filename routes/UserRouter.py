from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.Engine import get_db
from database.dtos import ProfileUpdateRequest, PasswordChangeRequest, APIResponse, \
    UserDetailUpdateRequest
from models import User, UserDetail
from utils.Security import get_current_user, verify_password, pwd_context

# Initialize the APIRouter for user-related operations
UserRouter = APIRouter()


# Route to get the current user's details
@UserRouter.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_detail = db.query(UserDetail).filter(UserDetail.user_id == current_user.user_id).first()

    if user_detail:
        data = {
            "fullname": current_user.fullname,
            "email": current_user.email,
            "age": user_detail.age,
            "height": user_detail.height,
            "weight": user_detail.weight
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
async def update_metrics(user_detail_update_request: UserDetailUpdateRequest,
                         current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_detail = db.query(UserDetail).filter(UserDetail.user_id == current_user.user_id).first()
    if not user_detail:
        user_detail = UserDetail(user_id=current_user.user_id)
        db.add(user_detail)

    user_detail.age = user_detail_update_request.age
    user_detail.height = user_detail_update_request.height
    user_detail.weight = user_detail_update_request.weight
    db.commit()
    db.refresh(user_detail)

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Metrics updated successfully",
        data={
            "age": user_detail.age,
            "height": user_detail.height,
            "weight": user_detail.weight
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

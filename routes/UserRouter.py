from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from database.dtos import UserCreateResponse, ProfileUpdateRequest, PasswordChangeRequest, APIResponse
from models import User
from utils.Security import get_current_user, verify_password, pwd_context

# Initialize the APIRouter for user-related operations
UserRouter = APIRouter()


# Route to get the current user's details
@UserRouter.get("/me", response_model=UserCreateResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return UserCreateResponse(fullname=current_user.fullname, email=current_user.email)


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

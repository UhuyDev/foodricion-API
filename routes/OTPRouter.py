from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status, Body, APIRouter
from sqlalchemy.orm import Session

import models
from database.Engine import get_db
from database.dtos import ForgotPasswordRequest, OTPVerificationRequest
from utils.OTP import generate_otp, send_otp_email, pwd_context

OTPRouter = APIRouter()


def datetime_to_timestamp(dt):
    return int(dt.timestamp())


def timestamp_to_datetime(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc)


@OTPRouter.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: ForgotPasswordRequest = Body(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate OTP
    otp = generate_otp()
    # Store OTP in database
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=3)
    db_otp = models.OTP(user_id=user.user_id, otp_code=otp, expires_at=datetime_to_timestamp(expire_time))
    db.add(db_otp)
    db.commit()

    # Send OTP email
    try:
        await send_otp_email(request.email, otp)
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail="Error sending email")

    return {"message": "OTP sent to your email"}


# Endpoint to verify OTP and reset password
@OTPRouter.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(request: OTPVerificationRequest = Body(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if OTP exists and is valid
    otp_record = db.query(models.OTP).filter(
        models.OTP.user_id == user.user_id,
        models.OTP.otp_code == request.otp,
        models.OTP.expires_at > datetime_to_timestamp(datetime.now(timezone.utc))
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Update user's password
    hashed_password = pwd_context.hash(request.new_password)
    user.password_hash = hashed_password

    # Delete the used OTP
    db.delete(otp_record)
    db.commit()

    return {"message": "Password reset successful"}

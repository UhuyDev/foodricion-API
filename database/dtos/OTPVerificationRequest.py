from pydantic import BaseModel, EmailStr


class OTPVerificationRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

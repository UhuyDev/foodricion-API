from pydantic import BaseModel, EmailStr


class OTPVerificationRequest(BaseModel):
    email: EmailStr
    otp: int
    new_password: str

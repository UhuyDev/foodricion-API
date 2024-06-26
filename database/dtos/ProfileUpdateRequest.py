from pydantic import BaseModel, EmailStr


class ProfileUpdateRequest(BaseModel):
    full_name: str
    email: EmailStr

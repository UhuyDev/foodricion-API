from pydantic import BaseModel, EmailStr


class UserCreateResponse(BaseModel):
    fullname: str
    email: EmailStr

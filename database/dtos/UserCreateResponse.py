from pydantic import BaseModel

class UserCreateResponse(BaseModel):
    fullname: str
    email: str
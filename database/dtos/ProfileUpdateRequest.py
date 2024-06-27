from pydantic import BaseModel

class ProfileUpdateRequest(BaseModel):
    full_name: str
    email: str
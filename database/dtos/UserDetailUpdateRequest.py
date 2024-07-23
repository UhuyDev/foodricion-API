from typing import Optional

from pydantic import BaseModel


class UserDetailUpdateRequest(BaseModel):
    age: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None

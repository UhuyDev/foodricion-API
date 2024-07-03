from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
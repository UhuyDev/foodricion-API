from pydantic import BaseModel


class BookmarkCreateRequest(BaseModel):
    food_id: int = None
    food_name: str = None

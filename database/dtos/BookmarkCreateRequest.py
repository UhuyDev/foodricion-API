from pydantic import BaseModel


class BookmarkCreateRequest(BaseModel):
    food_name: str

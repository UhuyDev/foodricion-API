from pydantic import BaseModel


class BookmarkDeleteRequest(BaseModel):
    bookmark_id: int

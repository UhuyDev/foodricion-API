from pydantic import BaseModel


class ChatbotHistoryCreateRequest(BaseModel):
    message: str
    response: str

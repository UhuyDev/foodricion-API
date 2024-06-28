from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.dtos import ChatbotHistoryCreateRequest
from database.Engine import get_db
from models import ChatbotConversation, User
from utils.Security import get_current_user

ChatbotRouter = APIRouter()


@ChatbotRouter.get("/chatbot-history", status_code=status.HTTP_200_OK)
async def read_chatbot_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatbot_history = db.query(ChatbotConversation).filter(
        ChatbotConversation.user_id == current_user.user_id).order_by(
        ChatbotConversation.timestamp.desc()).all()
    if not chatbot_history:
        raise HTTPException(status_code=404, detail='Chatbot history not found for this user')
    return chatbot_history


@ChatbotRouter.post("/chatbot-history", status_code=status.HTTP_201_CREATED)
async def create_chatbot_history(chatbot_data: ChatbotHistoryCreateRequest,
                                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_chatbot = ChatbotConversation(
        message=chatbot_data.message,
        response=chatbot_data.response,
        user_id=current_user.user_id
    )
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot

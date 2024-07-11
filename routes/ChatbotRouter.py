from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from database.dtos import ChatRequest, APIResponse
from models import ChatbotConversation, User
from utils.Chatbot import chatbot_response
from utils.Security import get_current_user

ChatbotRouter = APIRouter()


@ChatbotRouter.post("/chatbot")
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    response = await chatbot_response(request.user_input)

    # Save the chat to the database
    chat_entry = ChatbotConversation(
        user_id=current_user.user_id,
        message=request.user_input,
        response=response
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)

    return APIResponse(code=200,
                       message="Success",
                       data={"response": response})


@ChatbotRouter.get("/chatbot-history", status_code=status.HTTP_200_OK)
async def read_chatbot_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatbot_history = db.query(ChatbotConversation).filter(
        ChatbotConversation.user_id == current_user.user_id).order_by(
        ChatbotConversation.timestamp.desc()).all()
    if not chatbot_history:
        raise HTTPException(status_code=404, detail='Chatbot history not found for this user')

    # Convert the chatbot history to a list of dictionaries
    chatbot_history_data = []
    for chatbot in chatbot_history:
        chatbot_history_data.append({
            "user_id": chatbot.user_id,
            "message": chatbot.message,
            "response": chatbot.response,
            "timestamp": chatbot.timestamp.isoformat() if chatbot.timestamp else None
        })

    return APIResponse(code=200,
                       message="chatbot history retrieved successfully",
                       data=chatbot_history_data)

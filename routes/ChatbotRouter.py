from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.Engine import get_db
from database.dtos import ChatRequest, APIResponse
from models import ChatbotConversation, User
from utils.Chatbot import chatbot_response
from utils.Security import get_current_user

ChatbotRouter = APIRouter()


# Endpoint to interact with the chatbot
@ChatbotRouter.post("/chatbot", status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get the chatbot's response to the user's input
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

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Success",
        data={"response": response}
    )


# Endpoint to retrieve the chatbot history for the current user
@ChatbotRouter.get("/chatbot-history", status_code=status.HTTP_200_OK)
async def read_chatbot_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Query the database for the chatbot history of the current user, ordered by timestamp in descending order
    chatbot_history = db.query(ChatbotConversation).filter(
        ChatbotConversation.user_id == current_user.user_id).order_by(
        ChatbotConversation.timestamp.desc()).all()

    # Convert the chatbot history to a list of dictionaries
    chatbot_history_data = [
        {
            "user_id": chatbot.user_id,
            "message": chatbot.message,
            "response": chatbot.response,
            "timestamp": chatbot.timestamp
        }
        for chatbot in chatbot_history
    ]

    return APIResponse(
        code=status.HTTP_200_OK,
        message="Chatbot history retrieved successfully",
        data=chatbot_history_data
    )

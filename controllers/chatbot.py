from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import dotenv
from services.chatbot_service import ChatbotService

dotenv.load_dotenv()

router = APIRouter(prefix="/chat-bot", tags=["Chat Bot"])


class ChatbotRequest(BaseModel):
    """Request model cho chatbot"""
    chat_id: uuid.UUID
    message: str


@router.post("/")
def chatbot_reply(request: ChatbotRequest):
    """
    Endpoint xử lý tin nhắn chat
    
    Args:
        request: ChatbotRequest chứa chat_id và message
        
    Returns:
        Dict chứa reply từ chatbot
    """
    user_message_content = request.message.strip()
    return ChatbotService.process_chat(request.chat_id, user_message_content)
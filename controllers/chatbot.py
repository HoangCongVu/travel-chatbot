from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import dotenv
from services.chatbot_service import ChatbotService
from services.message import MessageService
from models.message import CreateMessagePayload
from utils.socket_manager import emit_socket_safely

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
    
    # Tạo và emit user message trước khi xử lý
    user_msg = MessageService.create_message(CreateMessagePayload(
        chat_id=request.chat_id,
        content=user_message_content,
        role="user"
    ))
    
    # 🔥 Emit socket event cho user message
    emit_socket_safely(str(request.chat_id), {
        "message_id": str(user_msg.id),
        "chat_id": str(request.chat_id),
        "content": user_message_content,
        "role": "user",
        "created_at": user_msg.created_at.isoformat() if user_msg.created_at else None,
        "meta_data": user_msg.meta_data
    })
    
    # Xử lý chatbot (sẽ tạo assistant message và emit)
    return ChatbotService.process_chat(request.chat_id, user_message_content)
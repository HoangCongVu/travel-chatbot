from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid
import dotenv
from services.chatbot_service import ChatbotService
from services.message import MessageService
from models.message import CreateMessagePayload
from utils.socket_manager import emit_socket_safely
from utils.context import ChatContext
from middleware.auth import get_current_user
from services.chat import ChatService

dotenv.load_dotenv()

router = APIRouter(prefix="/chat-bot", tags=["Chat Bot"])


class ChatbotRequest(BaseModel):
    """Request model cho chatbot"""
    chat_id: uuid.UUID
    message: str


class ChatbotAuthRequest(BaseModel):
    """Request model cho chatbot với auth"""
    chat_id: uuid.UUID
    message: str


@router.post("/")
def chatbot_reply(request: ChatbotRequest):
    """
    Endpoint xử lý tin nhắn chat (anonymous)
    
    Args:
        request: ChatbotRequest chứa chat_id và message
        
    Returns:
        Dict chứa reply từ chatbot
    """
    user_message_content = request.message.strip()
    
    # Lấy thông tin chat để xác định session_id
    chat = ChatService.get_chat(request.chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
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
    
    # ✅ SET CONTEXT cho request này (thread-safe)
    ChatContext.set(
        chat_id=str(request.chat_id),
        user_id=str(chat.user_id) if chat.user_id else None,
        session_id=str(chat.session_id) if chat.session_id else None
    )
    
    try:
        # Xử lý chatbot với session context
        result = ChatbotService.process_chat(
            chat_id=request.chat_id, 
            user_message=user_message_content,
            user_id=chat.user_id,  # Có thể None nếu anonymous
            session_id=chat.session_id
        )
        return result
    finally:
        # 🧹 Cleanup context sau khi xử lý xong
        ChatContext.clear()


@router.post("/auth")  
def chatbot_reply_auth(
    request: ChatbotAuthRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Endpoint xử lý tin nhắn chat (authenticated user)
    
    Args:
        request: ChatbotAuthRequest chứa chat_id và message
        current_user: User ID từ token
        
    Returns:
        Dict chứa reply từ chatbot
    """
    user_message_content = request.message.strip()
    
    # Convert current_user string to UUID
    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID in token")
    
    # Lấy thông tin chat để verify ownership
    chat = ChatService.get_chat(request.chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Verify user owns this chat
    if chat.user_id and chat.user_id != user_uuid:
        raise HTTPException(status_code=403, detail="Access denied to this chat")
    
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
    
    # ✅ SET CONTEXT cho request này (thread-safe)
    ChatContext.set(
        chat_id=str(request.chat_id),
        user_id=str(user_uuid),
        session_id=None  # Authenticated user không cần session_id
    )
    
    try:
        # Xử lý chatbot với user context
        result = ChatbotService.process_chat(
            chat_id=request.chat_id,
            user_message=user_message_content,
            user_id=user_uuid,
            session_id=None  # Authenticated user không cần session_id
        )
        return result
    finally:
        # 🧹 Cleanup context sau khi xử lý xong
        ChatContext.clear()
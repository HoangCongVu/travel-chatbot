import asyncio
from fastapi import APIRouter, HTTPException, Depends
from models.chat import CreateChatPayload, UpdateChatPayload, ChatModel
from models.message import CreateMessagePayload
from services.chat import ChatService
from services.message import MessageService
from pydantic import BaseModel
import uuid
from uuid import uuid4, UUID
from middleware.auth import get_current_user, get_current_admin
from utils.facebook_messenger import send_facebook_message

router = APIRouter(prefix="/chats", tags=["Chats"])

# Payload tạo chat
class ChatPayload(BaseModel):
    title: str

class AdminMessageRequest(BaseModel):
    content: str

# Payload khi tạo chat chưa đăng nhập (ẩn danh)
# class AnonymousChatPayload(BaseModel):
#     title: str

@router.post("/userchat", response_model=ChatModel)
def start_chat_session(
    payload: ChatPayload,
    current_user: str = Depends(get_current_user) 
):
    """
    Tạo chat khi người dùng đã đăng nhập
    """
    # override payload.user_id bằng current_user từ token
    full_payload = CreateChatPayload(
        user_id=current_user,           # lấy từ token, đảm bảo hợp lệ
        title=payload.title,
        session_id=uuid4()              # tạo session mới
    )
    return ChatService.create_chat(full_payload)

@router.post("/anonymouschat", response_model=ChatModel)
def create_anonymous_chat(payload: ChatPayload):
    """
    Người dùng chưa đăng nhập vẫn có thể tạo chat
    - Không có user_id
    - Sinh session_id ngẫu nhiên
    """
    full_payload = CreateChatPayload(
        user_id=None,
        title=payload.title,
        session_id=uuid.uuid4(),
    )
    return ChatService.create_chat(full_payload)

@router.post("", response_model=ChatModel)
def create_chat(payload: CreateChatPayload):
    return ChatService.create_chat(payload)


@router.get("", response_model=ChatModel)
def get_chat(chat_id: uuid.UUID):
    chat = ChatService.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.put("/update/{chat_id}", response_model=ChatModel)
def update_chat(chat_id: uuid.UUID, payload: UpdateChatPayload):
    chat = ChatService.update_chat(chat_id, payload)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("/delete/{chat_id}")
def delete_chat(chat_id: uuid.UUID):
    ChatService.delete_chat(chat_id)
    return {"message": "Chat deleted successfully"}

@router.get("/user/me", response_model=list[ChatModel])
def get_all_chats_by_user(current_user: str = Depends(get_current_user)):
    """
    Lấy danh sách chat của user dựa trên token (current_user)
    """
    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID in token")

    chats = ChatService.get_all_chats_by_user(user_uuid)
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found for this user")
    return chats

@router.get("/all", response_model=list[ChatModel])
def get_all_chats():
    chats = ChatService.get_all_chats()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats

@router.post("/{chat_id}/admin-message")
def send_admin_message(
    chat_id: uuid.UUID,
    payload: AdminMessageRequest,
    current_admin: str = Depends(get_current_admin)
) -> dict:
    """Cho phép admin gửi tin nhắn trực tiếp đến user trong chat."""
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    try:
        admin_uuid = uuid.UUID(current_admin)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    try:
        chat = ChatService.get_chat(chat_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = MessageService.create_message(
        CreateMessagePayload(
            chat_id=chat_id,
            content=content,
            role="admin",
            meta_data={
                "sender": "admin",
                "admin_id": str(admin_uuid)
            }
        )
    )

    delivery_result = {"status": "skipped", "reason": "No external channel"}

    if chat.platform == "facebook" and chat.external_user_id:
        try:
            delivery_result = asyncio.run(
                send_facebook_message(chat.external_user_id, content)
            )
        except Exception as send_error:
            delivery_result = {"status": "failed", "error": str(send_error)}

    return {
        "status": "success",
        "data": {
            "message": message,
            "delivery": delivery_result
        }
    }
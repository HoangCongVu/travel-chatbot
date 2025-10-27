from fastapi import APIRouter, HTTPException, Depends
from models.chat import CreateChatPayload, UpdateChatPayload, ChatModel
from services.chat import ChatService
from pydantic import BaseModel
import uuid
from uuid import uuid4, UUID
from middleware.auth import get_current_user

router = APIRouter(prefix="/chats", tags=["Chats"])

# Payload tạo chat
class ChatPayload(BaseModel):
    title: str

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


@router.put("", response_model=ChatModel)
def update_chat(chat_id: uuid.UUID, payload: UpdateChatPayload):
    chat = ChatService.update_chat(chat_id, payload)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("")
def delete_chat(chat_id: uuid.UUID):
    ChatService.delete_chat(chat_id)
    return {"message": "Chat deleted successfully"}

@router.get("/user/{user_id}", response_model=list[ChatModel])
def get_all_chats_by_user(user_id: uuid.UUID):
    chats = ChatService.get_all_chats_by_user(user_id)
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found for this user")
    return chats
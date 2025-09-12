from fastapi import APIRouter, HTTPException
from models.chat import CreateChatPayload, UpdateChatPayload, ChatModel
from services.chat import ChatService
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/chats", tags=["Chats"])

# Payload đơn giản hơn cho việc tạo chat
class SimpleChatPayload(BaseModel):
    user_id: uuid.UUID
    title: str

@router.post("/start-session", response_model=ChatModel)
def start_chat_session(payload: SimpleChatPayload):
    """Tạo chat session mới với session_id được tự động tạo"""
    full_payload = CreateChatPayload(
        user_id=payload.user_id,
        title=payload.title,
        session_id=uuid.uuid4()  # Tự động tạo session_id
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
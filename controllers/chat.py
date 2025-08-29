import uuid
from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.chat import CreateChat, UpdateChat, ChatModel
from services.chat import ChatService

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=ChatModel)
def create_chat(chat: CreateChat):
    return ChatService.create_chat(chat)


@router.get("/{chat_id}", response_model=ChatModel)
def get_chat(chat_id: uuid.UUID):
    chat = ChatService.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.put("/{chat_id}", response_model=ChatModel)
def update_chat(chat_id: uuid.UUID, chat: UpdateChat):
    updated = ChatService.update_chat(chat_id, chat)
    if not updated:
        raise HTTPException(status_code=404, detail="Chat not found")
    return updated


@router.delete("/{chat_id}", response_model=dict)
def delete_chat(chat_id: uuid.UUID):
    deleted = ChatService.delete_chat(chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}


@router.get("/user/{user_id}", response_model=List[ChatModel])
def get_chats_by_user(
    user_id: uuid.UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    return ChatService.get_chats_by_user(user_id=user_id, limit=limit, offset=offset)

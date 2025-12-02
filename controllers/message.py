from fastapi import APIRouter, HTTPException, status
from models.message import CreateMessagePayload, UpdateMessagePayload, MessageModel
from services.message import MessageService
from utils.socket_manager import emit_new_message
import uuid

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("", response_model=MessageModel, status_code=status.HTTP_201_CREATED)
async def create_message(payload: CreateMessagePayload):
    message = MessageService.create_message(payload)
    
    # 🔥 Emit socket event để notify real-time
    try:
        await emit_new_message(str(payload.chat_id), {
            "message_id": str(message.id),
            "chat_id": str(message.chat_id),
            "content": message.content,
            "role": message.role,
            "created_at": message.created_at.isoformat() if message.created_at else None,
            "meta_data": message.meta_data
        })
    except Exception as socket_error:
        print(f"⚠️ Socket emit failed: {socket_error}")
    
    return message


@router.get("", response_model=MessageModel)
def get_message(message_id: uuid.UUID):
    try:
        message = MessageService.get_message(message_id)
        return message
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


@router.put("", response_model=MessageModel)
def update_message(message_id: uuid.UUID, payload: UpdateMessagePayload):
    try:
        message = MessageService.update_message(message_id, payload)
        return message
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: uuid.UUID):
    try:
        MessageService.delete_message(message_id)
        return {"message": "Message deleted successfully"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

@router.get("/recent", response_model=list[MessageModel])
def get_recent_messages(chat_id: uuid.UUID, limit: int = 20):
    try:
        messages = MessageService.get_recent_messages(chat_id, limit)
        return messages
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found")

@router.get("/{chat_id}", response_model=list[MessageModel])
def get_chat_messages(chat_id: uuid.UUID):
    try:
        messages = MessageService.get_chat_messages(chat_id)
        return messages
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found")
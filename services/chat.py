import uuid
from typing import Optional, List
from models.chat import CreateChat, UpdateChat, ChatModel
from repositories.chat import ChatRepository


class ChatService:
    @staticmethod
    def create_chat(payload: CreateChat) -> ChatModel:
        return ChatRepository.create(payload)

    @staticmethod
    def get_chat(chat_id: uuid.UUID) -> Optional[ChatModel]:
        return ChatRepository.get(chat_id)

    @staticmethod
    def update_chat(chat_id: uuid.UUID, data: UpdateChat) -> Optional[ChatModel]:
        return ChatRepository.update(chat_id=chat_id, data=data)

    @staticmethod
    def delete_chat(chat_id: uuid.UUID) -> bool:
        return ChatRepository.delete(chat_id)

    @staticmethod
    def get_chats_by_user(
        user_id: uuid.UUID, limit: int = 100, offset: int = 0
    ) -> List[ChatModel]:
        return ChatRepository.get_all_by_user(user_id=user_id, limit=limit, offset=offset)

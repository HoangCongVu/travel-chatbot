import uuid
from models.chat import CreateChatPayload, UpdateChatPayload, ChatModel
from repositories.chat import ChatRepository


class ChatService:
    @staticmethod
    def create_chat(payload: CreateChatPayload) -> ChatModel:
        """
        ✅ Tạo chat mới
        - Nếu user_id có → gắn với tài khoản
        - Nếu không có → tạo chat ẩn danh với session_id
        """
        return ChatRepository.create(payload)

    @staticmethod
    def get_chat(chat_id: uuid.UUID) -> ChatModel:
        return ChatRepository.get_one(chat_id)

    @staticmethod
    def update_chat(chat_id: uuid.UUID, data: UpdateChatPayload) -> ChatModel:
        return ChatRepository.update(chat_id, data)

    @staticmethod
    def delete_chat(chat_id: uuid.UUID) -> None:
        return ChatRepository.delete(chat_id)

    @staticmethod
    def get_all_chats_by_user(user_id: uuid.UUID) -> list[ChatModel]:
        return ChatRepository.get_all_chat_by_user(user_id)

    @staticmethod
    def find_by_platform_id(platform: str, external_id: str) -> ChatModel | None:
        """
        ✅ Tìm chat theo platform và external_user_id
        """
        return ChatRepository.find_by_platform_and_external_id(platform, external_id)
    
    @staticmethod
    def get_all_chats() -> list[ChatModel]:
        return ChatRepository.get_all_chat()
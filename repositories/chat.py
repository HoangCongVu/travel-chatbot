import uuid
from db import Session
from models.chat import Chat, CreateChatPayload, UpdateChatPayload, ChatModel
from models.message import Message


class ChatRepository:
    @staticmethod
    def create(payload: CreateChatPayload) -> ChatModel:
        with Session() as session:
            chat_data = payload.model_dump()

            # ✅ Nếu không có session_id, tự tạo
            if not chat_data.get("session_id"):
                chat_data["session_id"] = uuid.uuid4()

            # ✅ Cho phép tạo chat khi chưa có user_id
            if not chat_data.get("user_id"):
                chat_data["user_id"] = None

            chat = Chat(**chat_data)
            session.add(chat)
            session.commit()
            session.refresh(chat)
            return ChatModel.model_validate(chat)

    @staticmethod
    def get_one(chat_id: uuid.UUID) -> ChatModel:
        with Session() as session:
            chat = session.get(Chat, chat_id)
            if not chat:
                raise ValueError(f"Chat with ID {chat_id} not found")
            return ChatModel.model_validate(chat)

    @staticmethod
    def update(chat_id: uuid.UUID, data: UpdateChatPayload) -> ChatModel:
        with Session() as session:
            chat = session.get(Chat, chat_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(chat, field, value)
            session.commit()
            session.refresh(chat)
            return ChatModel.model_validate(chat)

    @staticmethod
    def delete(chat_id: uuid.UUID):
        with Session() as session:
            # ✅ Xóa message trước
            session.query(Message).filter(Message.chat_id == chat_id).delete()

            chat = session.get(Chat, chat_id)
            if not chat:
                raise ValueError(f"Chat with ID {chat_id} not found")

            session.delete(chat)
            session.commit()

    @staticmethod
    def get_all_chat_by_user(user_id: uuid.UUID) -> list[ChatModel]:
        with Session() as session:
            chats = session.query(Chat).filter(Chat.user_id == user_id).all()
            return [ChatModel.model_validate(chat) for chat in chats]

    @staticmethod
    def get_all_chat_by_session(session_id: uuid.UUID) -> list[ChatModel]:
        """
        ✅ Lấy tất cả chat của người dùng chưa đăng nhập (dựa vào session_id)
        """
        with Session() as session:
            chats = session.query(Chat).filter(Chat.session_id == session_id).all()
            return [ChatModel.model_validate(chat) for chat in chats]

    @staticmethod
    def find_by_platform_and_external_id(platform: str, external_user_id: str) -> ChatModel | None:
        """
        ✅ Tìm chat theo platform và external_user_id (Facebook, Zalo, etc.)
        """
        with Session() as session:
            chat = session.query(Chat).filter(
                Chat.platform == platform,
                Chat.external_user_id == external_user_id
            ).first()
            
            if chat:
                return ChatModel.model_validate(chat)
            return None
    
    @staticmethod
    def get_all_chat() -> list[ChatModel]:
        with Session() as session:
            chats = session.query(Chat).all()
            return [ChatModel.model_validate(chat) for chat in chats]
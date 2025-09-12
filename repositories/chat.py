import uuid
from db import Session
from models.chat import Chat, CreateChatPayload, UpdateChatPayload, ChatModel
from models.message import Message


class ChatRepository:
    @staticmethod
    def create(payload: CreateChatPayload) -> ChatModel:
        with Session() as session:
            # Tự động tạo session_id nếu không được cung cấp
            chat_data = payload.model_dump()
            if not chat_data.get('session_id'):
                chat_data['session_id'] = uuid.uuid4()
            
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
            # Xóa tất cả message có chat_id này
            session.query(Message).filter(Message.chat_id == chat_id).delete()
            # Sau đó xóa chat
            chat = session.get(Chat, chat_id)
            session.delete(chat)
            session.commit()

    @staticmethod
    def get_all_chat_by_user(user_id: uuid.UUID) -> list[ChatModel]:
        with Session() as session:
            chats = session.query(Chat).filter(Chat.user_id == user_id).all()
            return [ChatModel.model_validate(chat) for chat in chats]
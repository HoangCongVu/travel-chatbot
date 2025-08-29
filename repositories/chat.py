import uuid
from typing import Optional, List
from models.chat import Chat, CreateChat, UpdateChat, ChatModel
from db import Session


class ChatRepository:
    @staticmethod
    def create(payload: CreateChat) -> ChatModel:
        with Session() as session:
            chat = Chat(**payload.model_dump())
            session.add(chat)
            session.commit()
            session.refresh(chat)
            return ChatModel.model_validate(chat)

    @staticmethod
    def get(chat_id: uuid.UUID) -> Optional[ChatModel]:
        with Session() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            return ChatModel.model_validate(chat) if chat else None

    @staticmethod
    def update(chat_id: uuid.UUID, data: UpdateChat) -> Optional[ChatModel]:
        with Session() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(chat, key, value)
            session.commit()
            session.refresh(chat)
            return ChatModel.model_validate(chat)

    @staticmethod
    def delete(chat_id: uuid.UUID) -> bool:
        with Session() as session:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                session.delete(chat)
                session.commit()
                return True
            return False

    @staticmethod
    def get_all_by_user(user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[ChatModel]:
        with Session() as session:
            chats = (
                session.query(Chat)
                .filter(Chat.user_id == user_id)
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [ChatModel.model_validate(chat) for chat in chats]

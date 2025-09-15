from typing import Optional
from datetime import datetime
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
import uuid
import sqlalchemy as sa
from models.user import UserTable
from db import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), ForeignKey(UserTable.id), nullable=False)
    session_id: Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class CreateChatPayload(BaseModel):
    user_id: uuid.UUID
    title: str 
    session_id: Optional[uuid.UUID] = None  # Optional, sẽ tự động tạo nếu không có 


class UpdateChatPayload(BaseModel):
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    title: Optional[str] = None 


class ChatModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    session_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
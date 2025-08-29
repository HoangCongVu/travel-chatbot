import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CreateChat(BaseModel):
    user_id: uuid.UUID
    session_id: uuid.UUID
    title: str 


class UpdateChat(BaseModel):
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    title: Optional[str] = None 
    model_config = ConfigDict(from_attributes=True)


class ChatModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    session_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
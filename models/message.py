from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    content = mapped_column(Text, nullable=False)
    role = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class MessageCreateModel(Base):
    chat_id: uuid.UUID
    content: str
    role: str

class MessagePydanticModel(Base):
    id: int
    chat_id: uuid.UUID
    content: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CreateMessageResponseModel(Base):
    message: MessagePydanticModel
    detail: str = "Message created successfully"

    class Config:
        orm_mode = True
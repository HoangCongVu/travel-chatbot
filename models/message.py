from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from db import Base

class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    content = mapped_column(Text, nullable=False)
    role = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
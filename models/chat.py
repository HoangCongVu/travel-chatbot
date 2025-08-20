import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from db import Base

class Chat(Base):
    __tablename__ = "chats"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id = mapped_column(UUID(as_uuid=True), nullable=False)
    title = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

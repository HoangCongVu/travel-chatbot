from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Doctors(Base):
    __tablename__ = "doctors"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    fullname = mapped_column(Text, nullable=False)
    phone_number = mapped_column(Text, nullable=False, unique=True)
    chat_id = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    department_id = mapped_column(Integer, ForeignKey("departments.id"), nullable=False)
    specialiazation = mapped_column(Text, nullable=False)
    biography = mapped_column(Text, nullable=True)
    email = mapped_column(Text, nullable=False, unique=True)
    image_url = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
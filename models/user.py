import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class UserTable(Base):
    __tablename__ = "users"

    id = Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number = Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email = Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    password_hash = Mapped[str] = mapped_column(Text, nullable=False)
    created_at = Mapped[datetime] = mapped_column(DateTime,
        default=func.now(), nullable=False
    )

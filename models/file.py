import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict


class FileTable(Base):
    __tablename__ = "files"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )
    admin_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("admins.id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class UploadResultModel(BaseModel):
    url: str
    message: str

  
class FileCreateModel(BaseModel):
    admin_id: uuid.UUID
    file_name: str
    file_url: str
    model_config = ConfigDict(
        from_attributes=True,
        str_min_length=1,
        str_strip_whitespace=True,
    )
class FileModel(BaseModel):
    id: uuid.UUID
    admin_id: uuid.UUID
    file_name: str
    file_url: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True) 

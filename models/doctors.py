from datetime import datetime
import uuid
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict


class DoctorTable(Base):
    __tablename__ = "doctors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False
    )
    specialization: Mapped[str] = mapped_column(String(255), nullable=False)
    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )


# ==================== Pydantic Schemas ====================

class CreateDoctorPayload(BaseModel):
    fullname: str
    phone_number: str
    department_id: uuid.UUID
    specialization: str
    biography: str | None = None
    email: str
    image_url: str | None = None


class UpdateDoctorPayload(BaseModel):
    fullname: str | None = None
    phone_number: str | None = None
    department_id: uuid.UUID | None = None
    specialization: str | None = None
    biography: str | None = None
    email: str | None = None
    image_url: str | None = None


class DoctorModel(BaseModel):
    id: uuid.UUID
    fullname: str
    phone_number: str
    department_id: uuid.UUID
    specialization: str
    biography: str | None
    email: str
    image_url: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

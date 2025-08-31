from datetime import datetime
from tokenize import Number
from pydantic import BaseModel
from sqlalchemy import String,DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from db import Base

class Schedules(Base):
    __tablename__ = "schedules"
    id : Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    doctor_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("doctors.id"), nullable=False)
    day_of_week : Mapped[str] = mapped_column(String(20), nullable=False)
    start_time : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CreateSchedules(BaseModel):
    doctor_id: uuid.UUID
    day_of_week: str
    start_time: datetime
    end_time: datetime

class UpdateSchedules(BaseModel):
    doctor_id: uuid.UUID | None = None
    day_of_week: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

class SchedulesModel(BaseModel):
    id : uuid.UUID
    doctor_id: uuid.UUID
    day_of_week: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
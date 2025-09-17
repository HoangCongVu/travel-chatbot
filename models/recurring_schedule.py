import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime, Date, Integer, ARRAY
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict


class RecurringSchedule(Base):
    __tablename__ = "recurring_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departure_schedules.id"), nullable=False)
    recurrence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    weekdays: Mapped[Optional[List[int]]] = mapped_column(ARRAY(Integer), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class CreateRecurringSchedule(BaseModel):
    schedule_id: uuid.UUID
    recurrence_type: str
    start_date: date
    end_date: date
    weekdays: Optional[List[int]] = None

class UpdateRecurringSchedule(BaseModel):
    schedule_id: Optional[uuid.UUID] = None
    recurrence_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    weekdays: Optional[List[int]] = None

class RecurringScheduleModel(BaseModel):
    id: uuid.UUID
    schedule_id: uuid.UUID
    recurrence_type: str
    start_date: date
    end_date: date
    weekdays: Optional[List[int]]
    model_config = ConfigDict(from_attributes=True)

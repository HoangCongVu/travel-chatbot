import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime, Date, Integer, ARRAY
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict

class SpecificDeparture(Base):
    __tablename__ = "specific_departures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departure_schedules.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class CreateSpecificDeparturePayload(BaseModel):
    schedule_id: uuid.UUID
    date: Optional[date]


class UpdateSpecificDeparturePayload(BaseModel):
    id: uuid.UUID | None = None
    schedule_id: uuid.UUID | None = None
    date: Optional[date] = None


class SpecificDepartureModel(BaseModel):
    id: uuid.UUID
    schedule_id: uuid.UUID
    date: date
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

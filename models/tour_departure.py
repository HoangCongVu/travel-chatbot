import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict


class TourDeparture(Base):
    __tablename__ = "tour_departures"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), nullable=False)
    tour_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tours.id"), nullable=False)
    departure_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )



class CreateTourDeparturePayload(BaseModel):
    tour_id: uuid.UUID
    departure_name: str


class UpdateTourDeparturePayload(BaseModel):
    tour_id: uuid.UUID| None = None
    departure_name: str | None = None


class TourDepartureModel(BaseModel):
    id: uuid.UUID
    tour_id: uuid.UUID
    departure_name: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

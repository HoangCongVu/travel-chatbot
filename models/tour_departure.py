import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict
from pgvector.sqlalchemy import Vector


class TourDeparture(Base):
    __tablename__ = "tour_departures"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    tour_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tours.id"), nullable=False)
    departure_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tour_departure_embedding_vector: Mapped[list[float]] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )



class CreateTourDeparture(BaseModel):
    tour_id: uuid.UUID
    departure_name: str


class UpdateTourDeparture(BaseModel):
    id: uuid.UUID | None = None
    tour_id: uuid.UUID| None = None
    departure_name: str | None = None


class TourDepartureModel(BaseModel):
    id: uuid.UUID
    tour_id: uuid.UUID
    departure_name: str
    tour_departure_embedding: Optional[list[float]] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SearchTourDeparture(BaseModel):
    id: uuid.UUID
    tour_id: uuid.UUID
    departure_name: str
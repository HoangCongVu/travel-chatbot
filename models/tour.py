import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict
from pgvector.sqlalchemy import Vector


class TourTable(Base):
    __tablename__ = "tours"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    tour_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tour_type_id: Mapped[int] = mapped_column(ForeignKey("tour_types.id"), nullable=False)
    days: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    highlight: Mapped[str] = mapped_column(Text, nullable=False)
    itinerary_url: Mapped[str] = mapped_column(Text, nullable=False)
    detail_url: Mapped[str] = mapped_column(Text, nullable=False)
    promotion_info: Mapped[str] = mapped_column(Text, nullable=False)
    price_type: Mapped[str] = mapped_column(String(50), nullable=False)
    tour_embedding_vector: Mapped[list[float]] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class TourModel(BaseModel):
    id: uuid.UUID
    tour_name: str
    tour_type_id: int
    days: int
    description: str
    highlight: str
    itinerary_url: str
    detail_url: str
    promotion_info: str
    price_type: str
    tour_embedding_vector: Optional[list[float]] = None
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class TourCreateModel(BaseModel):
    tour_name: str
    tour_type_id: int
    days: int
    description: str
    highlight: str
    itinerary_url: str
    detail_url: str
    promotion_info: str
    price_type: str


class TourUpdateModel(BaseModel):
    tour_name: Optional[str] = None
    tour_type_id: Optional[int] = None
    days: Optional[int] = None
    description: Optional[str] = None
    highlight: Optional[str] = None
    itinerary_url: Optional[str] = None
    detail_url: Optional[str] = None
    promotion_info: Optional[str] = None
    price_type: Optional[str] = None

class SearchTour(BaseModel):
    id: uuid.UUID
    tour_name: str
    days: int
    description: str
    highlight: str
    itinerary_url: str = None
    detail_url: str = None
    promotion_info: str = None
    price_type: str
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    

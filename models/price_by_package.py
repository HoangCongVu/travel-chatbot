import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, func, ForeignKey, TIMESTAMP, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict


class PriceByPackage(Base):
    __tablename__ = "price_by_packages"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tour_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tours.id"), nullable=False)
    package_name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class CreatePriceByPackagePayload(BaseModel):
    tour_id: uuid.UUID
    package_name: str
    price: float


class UpdatePriceByPackagePayload(BaseModel):
    tour_id: uuid.UUID | None = None
    package_name: str | None = None
    price: float | None = None


class PriceByPackageModel(BaseModel):
    id: uuid.UUID 
    tour_id: uuid.UUID
    package_name: str
    price: float
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
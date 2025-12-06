import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, Text, ForeignKey, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, ConfigDict
from db import Base


class PaymentTable(Base):
    __tablename__ = "payments"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id"),
        nullable=False 
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False, server_default="sepay")
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="pending")
    transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_data: Mapped[dict | None] = mapped_column(JSONB(astext_type=Text()), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class PaymentModel(BaseModel):
    id: uuid.UUID
    booking_id: uuid.UUID
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: Optional[str] = None
    payment_url: Optional[str] = None
    meta_data: Optional[dict] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PaymentCreateModel(BaseModel):
    booking_id: uuid.UUID
    amount: float = Field(ge=0)
    payment_method: str = "sepay"
    payment_status: str = "pending"
    transaction_id: Optional[str] = None
    payment_url: Optional[str] = None
    meta_data: Optional[dict] = None
    paid_at: Optional[datetime] = None


class PaymentUpdateModel(BaseModel):
    amount: Optional[float] = Field(None, ge=0)
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    transaction_id: Optional[str] = None
    payment_url: Optional[str] = None
    meta_data: Optional[dict] = None
    paid_at: Optional[datetime] = None
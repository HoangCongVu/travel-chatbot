import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Numeric, Text, ForeignKey, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, ConfigDict
from db import Base


class BookingTable(Base):
    __tablename__ = "bookings"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True 
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    tour_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tours.id"), nullable=False)
    cart_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cart_items.id"),
        nullable=False
    )
    guest_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    guest_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    guest_email: Mapped[str | None] = mapped_column(String(50), nullable=True)
    adult_count: Mapped[int] = mapped_column(Integer, nullable=False)
    child_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="pending")
    special_request: Mapped[str | None] = mapped_column(Text, nullable=True) 
    meta_data: Mapped[dict | None] = mapped_column(JSONB(astext_type=Text()), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class BookingModel(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    tour_id: uuid.UUID
    cart_item_id: uuid.UUID
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    adult_count: int
    child_count: int
    total_price: float
    status: str
    special_request: Optional[str] = None
    meta_data: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BookingCreateModel(BaseModel):
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    tour_id: uuid.UUID
    cart_item_id: uuid.UUID
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    adult_count: int = Field(ge=0)
    child_count: int = Field(ge=0)
    total_price: float = Field(ge=0)
    status: str = "pending"
    special_request: Optional[str] = None
    meta_data: Optional[dict] = None


class BookingUpdateModel(BaseModel):
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    cart_item_id: Optional[uuid.UUID] = None
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    adult_count: Optional[int] = Field(None, ge=0)
    child_count: Optional[int] = Field(None, ge=0)
    total_price: Optional[float] = Field(None, ge=0)
    status: Optional[str] = None
    special_request: Optional[str] = None
    meta_data: Optional[dict] = None


class BookingWithCartItemModel(BaseModel):
    """Model for booking with cart item details"""
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    tour_id: uuid.UUID
    cart_item_id: uuid.UUID
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    adult_count: int
    child_count: int
    total_price: float
    status: str
    special_request: Optional[str] = None
    
    # Cart item details
    cart_item: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)


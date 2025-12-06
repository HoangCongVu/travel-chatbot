import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import Integer, Numeric, Date, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field, ConfigDict
from db import Base


class CartItemTable(Base):
    __tablename__ = "cart_items"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False
    )
    tour_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tours.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_snapshot: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    travel_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CartItemModel(BaseModel):
    id: uuid.UUID
    cart_id: uuid.UUID
    tour_id: uuid.UUID
    tour_name: str | None = None  # Tên tour (join từ tours table)
    quantity: int
    price_snapshot: float
    travel_date: date
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CartItemCreateModel(BaseModel):
    cart_id: uuid.UUID
    tour_id: uuid.UUID
    quantity: int = Field(ge=1, description="Số lượng")
    price_snapshot: float = Field(ge=0, description="Giá tại thời điểm thêm vào giỏ")
    travel_date: date = Field(description="Ngày khởi hành")


class CartItemUpdateModel(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    price_snapshot: Optional[float] = Field(None, ge=0)
    travel_date: Optional[date] = None

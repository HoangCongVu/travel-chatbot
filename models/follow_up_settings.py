"""
Model cho bảng follow_up_settings - Lưu cấu hình follow-up
"""
import uuid
from datetime import datetime
from sqlalchemy import Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict


class FollowUpSettings(Base):
    __tablename__ = "follow_up_settings"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey('admins.id', ondelete='SET NULL'), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    delay_minutes: Mapped[int] = mapped_column(Integer, nullable=False, server_default='30')
    max_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default='3')
    active_hours_start: Mapped[int] = mapped_column(Integer, nullable=False, server_default='8')
    active_hours_end: Mapped[int] = mapped_column(Integer, nullable=False, server_default='22')
    scan_interval_minutes: Mapped[int] = mapped_column(Integer, nullable=False, server_default='1')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class FollowUpSettingsResponse(BaseModel):
    """Response model cho follow-up settings"""
    id: uuid.UUID
    admin_id: uuid.UUID | None
    is_enabled: bool
    delay_minutes: int
    max_count: int
    active_hours_start: int
    active_hours_end: int
    scan_interval_minutes: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UpdateFollowUpSettingsRequest(BaseModel):
    """Request model để update settings"""
    is_enabled: bool | None = None
    delay_minutes: int | None = None
    max_count: int | None = None
    active_hours_start: int | None = None
    active_hours_end: int | None = None
    scan_interval_minutes: int | None = None

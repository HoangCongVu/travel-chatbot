import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from pydantic import BaseModel, ConfigDict

class TourTypeTable(Base):
    __tablename__ = "tour_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class CreateTourType(BaseModel):
    id: int
    type_name: str

class UpdateTourType(BaseModel):
    id: int | None = None
    type_name: str | None = None

class TourTypeModel(BaseModel):
    id: int
    type_name: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
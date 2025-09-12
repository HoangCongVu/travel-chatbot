import uuid
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from pydantic import BaseModel, Field, ConfigDict
from models.tour import TourTable


class Base(DeclarativeBase):
    pass


class DepartureSchedule(Base):
    __tablename__ = "departure_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tour_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(TourTable.id), nullable=False)
    schedule_type: Mapped[str] = mapped_column(String(50), nullable=False) 
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class CreateDepartureSchedulePayload(BaseModel):
    tour_id: uuid.UUID
    schedule_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UpdateDepartureSchedulePayload(BaseModel):
    tour_id: uuid.UUID | None = None
    schedule_type: str | None = None
    model_config = ConfigDict(from_attributes=True)


class DepartureScheduleModel(BaseModel):
    id: uuid.UUID
    tour_id: uuid.UUID
    schedule_type: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
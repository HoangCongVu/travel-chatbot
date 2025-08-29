from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column , Mapped
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Appointments(Base):
    __tablename__ = "appointments"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    doctor_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("doctors.id"), nullable=False)
    department_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("departments.id"), nullable=False)
    appointment_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    appointment_time : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status : Mapped[str] = mapped_column(String(40), nullable=False, default="WAITING")
    note : Mapped[str] = mapped_column(Text, nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CreateAppointments(BaseModel):
    user_id: uuid.UUID
    doctor_id: uuid.UUID
    department_id: uuid.UUID
    appointment_date: datetime
    appointment_time: datetime
    note: str | None = None

class UpdateAppointments(BaseModel):
    user_id: uuid.UUID | None = None
    doctor_id: uuid.UUID | None = None
    department_id: uuid.UUID | None = None
    appointment_date: datetime | None = None
    appointment_time: datetime | None = None
    status: str | None = None
    note: str | None = None
    model_config = ConfigDict(from_attributes=True)

class AppointmentsModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    doctor_id: uuid.UUID
    department_id: uuid.UUID
    appointment_date: datetime
    appointment_time: datetime
    status: str
    note: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
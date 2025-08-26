from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Appointments(Base):
    __tablename__ = "appointments"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = mapped_column(Integer, ForeignKey("doctors.id"), nullable=False)
    department_id = mapped_column(Integer, ForeignKey("departments.id"), nullable=False)
    status = mapped_column(Text, nullable=False)
    appointment_time = mapped_column(DateTime(timezone=True), nullable=False)
    appointment_date = mapped_column(DateTime(timezone=True), nullable=False)
    note = mapped_column(Text, nullable=True)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Services(Base):
    __tablename__ = "services"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    services_name = mapped_column(Text, nullable=False, unique=True)
    department_id = mapped_column(Integer, ForeignKey("departments.id"), nullable=False)
    description = mapped_column(Text, nullable=False)
    price = mapped_column(Integer, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
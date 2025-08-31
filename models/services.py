from datetime import datetime
from tokenize import Number
from sqlalchemy import Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column , Mapped
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from db import Base
from pydantic import BaseModel, ConfigDict

class Services(Base):
    __tablename__ = "services"

    id : Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    services_name : Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    department_id : Mapped[uuid.UUID]= mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=False)
    price : Mapped[float] = mapped_column(Number, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CreateServices(BaseModel):
    services_name: str
    department_id: uuid.UUID
    description: str
    price: float

class UpdateServices(BaseModel):
    services_name: str | None = None
    department_id: uuid.UUID | None = None
    description: str | None = None
    price: float | None = None


class ServicesModel(BaseModel):
    id: uuid.UUID
    services_name: str
    department_id: uuid.UUID
    description: str
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True
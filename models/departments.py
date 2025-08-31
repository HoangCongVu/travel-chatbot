
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column , Mapped
from sqlalchemy import String
from db import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID as pgUUID

class Departments(Base):
    __tablename__ = "departments"

    id : Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    department_name : Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description : Mapped[str] = mapped_column(Text, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CreateDepartments(BaseModel):
    department_name: str
    description: str

class UpdateDepartments(BaseModel):
    department_name: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class DepartmentsModel(BaseModel):
    id: uuid.UUID
    department_name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
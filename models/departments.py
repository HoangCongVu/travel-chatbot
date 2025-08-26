from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from db import Base

class Departments(Base):
    __tablename__ = "departments"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    description = mapped_column(Text, nullable=False, unique=True)
    department_name = mapped_column(Text, nullable=False, unique=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) 
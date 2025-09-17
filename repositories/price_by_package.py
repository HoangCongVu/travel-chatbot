import uuid
from db import Session
from datetime import datetime, timezone
from models.price_by_package import (
    PriceByPackage,
    CreatePriceByPackage,
    UpdatePriceByPackage,
    PriceByPackageModel
)


class PriceByPackageRepository:
    @staticmethod
    def create(payload: CreatePriceByPackage) -> PriceByPackageModel:
        with Session() as session:
            record = PriceByPackage(id=uuid.uuid4(), **payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(record)
            session.commit()
            session.refresh(record)
            return PriceByPackageModel.model_validate(record)

    @staticmethod
    def get_one(record_id: uuid.UUID) -> PriceByPackageModel:
        with Session() as session:
            record = session.get(PriceByPackage, record_id)
            return PriceByPackageModel.model_validate(record)

    @staticmethod
    def update(record_id: uuid.UUID, data: UpdatePriceByPackage) -> PriceByPackageModel:
        with Session() as session:
            record = session.get(PriceByPackage, record_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(record, field, value)
            session.commit()
            session.refresh(record)
            return PriceByPackageModel.model_validate(record)

    @staticmethod
    def delete(record_id: uuid.UUID):
        with Session() as session:
            record = session.get(PriceByPackage, record_id)
            session.delete(record)
            session.commit()
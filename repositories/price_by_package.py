import uuid
from db import Session
from models.price_by_package import (
    PriceByPackage,
    CreatePriceByPackagePayload,
    UpdatePriceByPackagePayload,
    PriceByPackageModel
)


class PriceByPackageRepository:
    @staticmethod
    def create(payload: CreatePriceByPackagePayload) -> PriceByPackageModel:
        with Session() as session:
            record = PriceByPackage(**payload.model_dump())
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
    def update(record_id: uuid.UUID, data: UpdatePriceByPackagePayload) -> PriceByPackageModel:
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
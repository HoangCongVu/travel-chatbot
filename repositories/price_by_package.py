import uuid
from db import Session
from datetime import datetime, timezone
from models.price_by_package import PriceByPackage, CreatePriceByPackage, UpdatePriceByPackage, PriceByPackageModel


class PriceByPackageRepository:
    @staticmethod
    def create(payload: CreatePriceByPackage) -> PriceByPackageModel:
        with Session() as session:
            record = PriceByPackage(id=uuid.uuid4(), **payload.model_dump())
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
    
    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[PriceByPackageModel]:
        with Session() as session:
            records = session.query(PriceByPackage).filter(PriceByPackage.tour_id == tour_id).all()
            return [PriceByPackageModel.model_validate(r) for r in records]

    @staticmethod
    def get_all() -> list[PriceByPackageModel]:
        with Session() as session:
            records = session.query(PriceByPackage).all()
            return [PriceByPackageModel.model_validate(r) for r in records][::-1]
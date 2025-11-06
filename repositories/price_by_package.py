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
    def update_by_tour_id(tour_id: uuid.UUID, data: UpdatePriceByPackage) -> list[PriceByPackageModel]:
        with Session() as session:
            records = session.query(PriceByPackage).filter(PriceByPackage.tour_id == tour_id).all()
            if not records:
                return []
            
            updated_records = []
            for record in records:
                for field, value in data.model_dump(exclude_unset=True).items():
                    setattr(record, field, value)
                updated_records.append(PriceByPackageModel.model_validate(record))
            
            session.commit()
            return updated_records

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
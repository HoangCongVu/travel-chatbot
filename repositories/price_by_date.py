import uuid
from db import Session
from datetime import datetime, timezone
from models.price_by_date import (
    PriceByDate,
    CreatePriceByDatePayload,
    UpdatePriceByDatePayload,
    PriceByDateModel
)

class PriceByDateRepository:
    @staticmethod
    def create(payload: CreatePriceByDatePayload) -> PriceByDateModel:
        with Session() as session:
            price = PriceByDate(**payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(price)
            session.commit()
            session.refresh(price)
            return PriceByDateModel.model_validate(price.__dict__)

    @staticmethod
    def get_one(price_id: uuid.UUID) -> PriceByDateModel:
        with Session() as session:
            price = session.query(PriceByDate).filter(PriceByDate.id == price_id).first()
            if price:
                return PriceByDateModel.from_orm(price)
            return " "
        
    
    @staticmethod
    def update(price_id: uuid.UUID, data: UpdatePriceByDatePayload) -> PriceByDateModel:
        with Session() as session:
            price = session.get(PriceByDate, price_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(price, field, value)
            session.commit()
            session.refresh(price)
            return PriceByDateModel.model_validate(price)

    @staticmethod
    def delete(price_id: uuid.UUID):
        with Session() as session:
            price = session.get(PriceByDate, price_id)
            session.delete(price)
            session.commit()
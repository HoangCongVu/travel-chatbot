import uuid
from db import Session
from datetime import datetime, timezone
from models.price_by_date import PriceByDate, CreatePriceByDate, UpdatePriceByDate, PriceByDateModel


class PriceByDateRepository:
    @staticmethod
    def create(payload: CreatePriceByDate) -> PriceByDateModel:
        with Session() as session:
            price = PriceByDate(id=uuid.uuid4(), **payload.model_dump())
            session.add(price)
            session.commit()
            session.refresh(price)
            return PriceByDateModel.model_validate(price.__dict__)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, data: UpdatePriceByDate) -> list[PriceByDateModel]:
        with Session() as session:
            prices = session.query(PriceByDate).filter(PriceByDate.tour_id == tour_id).all()
            if not prices:
                return []
            
            updated_prices = []
            for price in prices:
                for field, value in data.model_dump(exclude_unset=True).items():
                    setattr(price, field, value)
                updated_prices.append(PriceByDateModel.model_validate(price))
            
            session.commit()
            return updated_prices

    @staticmethod
    def delete(price_id: uuid.UUID):
        with Session() as session:
            price = session.get(PriceByDate, price_id)
            session.delete(price)
            session.commit()
    
    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[PriceByDateModel]:
        with Session() as session:
            prices = session.query(PriceByDate).filter(PriceByDate.tour_id == tour_id).all()
            return [PriceByDateModel.model_validate(p) for p in prices]

    @staticmethod
    def get_all() -> list[PriceByDateModel]:
        with Session() as session:
            prices = session.query(PriceByDate).all()
            return [PriceByDateModel.model_validate(p) for p in prices][::-1]
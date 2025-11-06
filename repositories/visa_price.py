import uuid
from db import Session
from datetime import datetime, timezone
from models.visa_price import CreateVisaPrice, VisaPriceModel, VisaPriceTable

class VisaPriceRepository():
    @staticmethod
    def create(payload: CreateVisaPrice) -> VisaPriceModel:
        with Session() as session:
            visa_price = VisaPriceTable(id=uuid.uuid4(), **payload.model_dump())
            session.add(visa_price)
            session.commit()
            session.refresh(visa_price)
            return VisaPriceModel.model_validate(visa_price)
    
    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, data: CreateVisaPrice):
        with Session() as session:
            visa_prices = session.query(VisaPriceTable).filter(VisaPriceTable.tour_id == tour_id).all()
            if not visa_prices:
                return []
            updated_visa_prices = []
            for visa_price in visa_prices:
                for key, value in data.model_dump().items():
                    setattr(visa_price, key, value)
                updated_visa_prices.append(VisaPriceModel.model_validate(visa_price))
            session.commit()
            return updated_visa_prices
    
    @staticmethod
    def delete(visa_price_id: uuid.UUID):
        with Session() as session:
            visa_price = session.query(VisaPriceTable).filter(VisaPriceTable.id == visa_price_id).first()
            if visa_price:
                session.delete(visa_price)
                session.commit()
            return visa_price

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[VisaPriceModel]:
        with Session() as session:
            visa_prices = session.query(VisaPriceTable).filter(VisaPriceTable.tour_id == tour_id).all()
            return [VisaPriceModel.model_validate(v) for v in visa_prices]

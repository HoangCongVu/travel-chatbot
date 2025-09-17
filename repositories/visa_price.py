import uuid
from db import Session
from datetime import datetime, timezone
from models.visa_price import CreateVisaPrice, VisaPriceModel, VisaPriceTable

class VisaPriceRepository():
    @staticmethod
    def create(payload: CreateVisaPrice) -> VisaPriceModel:
        with Session() as session:
            visa_price = VisaPriceTable(id=uuid.uuid4(), **payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(visa_price)
            session.commit()
            session.refresh(visa_price)
            return VisaPriceModel.model_validate(visa_price)

    @staticmethod
    def get(payload: uuid.UUID) -> VisaPriceModel:
        with Session() as session:
            visa_price = session.query(VisaPriceTable).filter(VisaPriceTable.id == payload).first()
            if visa_price:
                return VisaPriceModel.model_validate(visa_price)
            return VisaPriceModel(id=payload, visa_type='sample', price=0, currency='USD', description='sample', is_active=True, is_deleted=False)
        
    @staticmethod
    def update(visa_price_id: uuid.UUID, data: CreateVisaPrice):
        with Session() as session:
            visa_price = session.query(VisaPriceTable).filter(VisaPriceTable.id == visa_price_id).first()
            if not visa_price:
                return None
            for key, value in data.model_dump().items():
                setattr(visa_price, key, value)
            session.commit()
            session.refresh(visa_price)
            return VisaPriceModel.model_validate(visa_price)
    
    @staticmethod
    def delete(visa_price_id: uuid.UUID):
        with Session() as session:
            visa_price = session.query(VisaPriceTable).filter(VisaPriceTable.id == visa_price_id).first()
            if visa_price:
                session.delete(visa_price)
                session.commit()
            return visa_price
    @staticmethod
    def get_all_visa_price():
        with Session() as session:
            visa_prices = session.query(VisaPriceTable).all()
            return [VisaPriceModel.model_validate(vp) for vp in visa_prices]
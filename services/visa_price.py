import uuid
from models.visa_price import CreateVisaPrice, VisaPriceModel
from repositories.visa_price import VisaPriceRepository

class VisaPriceService():
    @staticmethod
    def create(payload: CreateVisaPrice):
        return VisaPriceRepository.create(payload)
    
    @staticmethod
    def get(payload: uuid.UUID):
        return VisaPriceRepository.get(payload)
    
    @staticmethod
    def update(visa_price_id: uuid.UUID, payload: CreateVisaPrice):
        return VisaPriceRepository.update(visa_price_id, payload)

    @staticmethod
    def delete(visa_price_id: uuid.UUID):
        VisaPriceRepository.delete(visa_price_id)
        return "Visa Price deleted successfully"
    @staticmethod
    def get_all():
        return VisaPriceRepository.get_all_visa_price()
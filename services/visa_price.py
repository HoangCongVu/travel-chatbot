import uuid
from models.visa_price import CreateVisaPrice, VisaPriceModel
from repositories.visa_price import VisaPriceRepository

class VisaPriceService():
    @staticmethod
    def create_visa_price(payload: CreateVisaPrice):
        return VisaPriceRepository.create(payload)
    
    @staticmethod
    def get_visa_price(payload: uuid.UUID):
        return VisaPriceRepository.get(payload)
    
    @staticmethod
    def update_visa_price(visa_price_id: uuid.UUID, data: CreateVisaPrice):
        return VisaPriceRepository.get(visa_price_id)
    
    @staticmethod
    def delete_visa_price():
        VisaPriceRepository.delete()
        return "Visa Price deleted successfully"
    @staticmethod
    def get_all_visa_price():
        return VisaPriceRepository.get_all_visa_price()
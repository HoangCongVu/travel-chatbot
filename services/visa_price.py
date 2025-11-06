import uuid
from models.visa_price import CreateVisaPrice, VisaPriceModel
from repositories.visa_price import VisaPriceRepository

class VisaPriceService():
    @staticmethod
    def create(payload: CreateVisaPrice):
        return VisaPriceRepository.create(payload)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: CreateVisaPrice):
        return VisaPriceRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(visa_price_id: uuid.UUID):
        VisaPriceRepository.delete(visa_price_id)
        return "Visa Price deleted successfully"
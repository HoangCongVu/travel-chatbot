import uuid
from models.price_by_date import CreatePriceByDate, UpdatePriceByDate, PriceByDateModel
from repositories.price_by_date import PriceByDateRepository


class PriceByDateService:
    @staticmethod
    def create(payload: CreatePriceByDate) -> PriceByDateModel:
        return PriceByDateRepository.create(payload)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: UpdatePriceByDate) -> list[PriceByDateModel]:
        return PriceByDateRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(price_id: uuid.UUID):
        return PriceByDateRepository.delete(price_id)
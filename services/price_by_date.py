import uuid
from models.price_by_date import (
    CreatePriceByDate,
    UpdatePriceByDate,
    PriceByDateModel
)
from repositories.price_by_date import PriceByDateRepository


class PriceByDateService:
    @staticmethod
    def create(payload: CreatePriceByDate) -> PriceByDateModel:
        return PriceByDateRepository.create(payload)

    @staticmethod
    def get(price_id: uuid.UUID) -> PriceByDateModel:
        return PriceByDateRepository.get_one(price_id)

    @staticmethod
    def update(price_id: uuid.UUID, payload: UpdatePriceByDate) -> PriceByDateModel:
        return PriceByDateRepository.update(price_id, payload)

    @staticmethod
    def delete(price_id: uuid.UUID):
        return PriceByDateRepository.delete(price_id)
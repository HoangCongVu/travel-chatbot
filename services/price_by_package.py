import uuid
from models.price_by_package import (
    CreatePriceByPackagePayload,
    UpdatePriceByPackagePayload,
    PriceByPackageModel
)
from repositories.price_by_package import PriceByPackageRepository


class PriceByPackageService:
    @staticmethod
    def create(payload: CreatePriceByPackagePayload) -> PriceByPackageModel:
        return PriceByPackageRepository.create(payload)

    @staticmethod
    def get(record_id: uuid.UUID) -> PriceByPackageModel:
        return PriceByPackageRepository.get_one(record_id)

    @staticmethod
    def update(record_id: uuid.UUID, payload: UpdatePriceByPackagePayload) -> PriceByPackageModel:
        return PriceByPackageRepository.update(record_id, payload)

    @staticmethod
    def delete(record_id: uuid.UUID):
        return PriceByPackageRepository.delete(record_id)
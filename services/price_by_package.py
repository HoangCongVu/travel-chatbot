import uuid
from models.price_by_package import CreatePriceByPackage, UpdatePriceByPackage, PriceByPackageModel
from repositories.price_by_package import PriceByPackageRepository


class PriceByPackageService:
    @staticmethod
    def create(payload: CreatePriceByPackage) -> PriceByPackageModel:
        return PriceByPackageRepository.create(payload)
    
    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: UpdatePriceByPackage) -> list[PriceByPackageModel]:
        return PriceByPackageRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(record_id: uuid.UUID):
        return PriceByPackageRepository.delete(record_id)
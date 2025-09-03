from repositories.tour_type import TourTypeRepository
from models.tour_type import (
    CreateTourType,
    UpdateTourType,
    TourTypeModel
)


class TourTypeService:
    @staticmethod
    def create(payload: CreateTourType) -> TourTypeModel:
        return TourTypeRepository.create(payload)

    @staticmethod
    def get(type_id: int) -> TourTypeModel:
        return TourTypeRepository.get_one(type_id)

    @staticmethod
    def update(type_id: int, payload: UpdateTourType) -> TourTypeModel:
        return TourTypeRepository.update(type_id, payload)

    @staticmethod
    def delete(type_id: int):
        return TourTypeRepository.delete(type_id)
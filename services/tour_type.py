import uuid
from models.tour_type import (
    CreateTourType,
    UpdateTourType,
    TourTypeModel
)
from repositories.tour_type import TourTypeRepository


class TourTypeService:
    @staticmethod
    def create(payload: CreateTourType) -> TourTypeModel:
        return TourTypeRepository.create(payload)

    @staticmethod
    def get(type_id: int) -> TourTypeModel | None:
        return TourTypeRepository.get_one(type_id)
    
    @staticmethod
    def get_by_name(type_name: str) -> TourTypeModel | None:
        return TourTypeRepository.get_by_name(type_name)

    @staticmethod
    def update(type_id: int, payload: UpdateTourType) -> TourTypeModel:
        return TourTypeRepository.update(type_id, payload)

    @staticmethod
    def delete(type_id: int):
        return TourTypeRepository.delete(type_id)
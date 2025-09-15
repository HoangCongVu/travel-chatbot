import uuid
from models.specific_departure import (
    CreateSpecificDeparturePayload,
    UpdateSpecificDeparturePayload,
    SpecificDepartureModel
)
from repositories.specific_departure import SpecificDepartureRepository


class SpecificDepartureService:
    @staticmethod
    def create(payload: CreateSpecificDeparturePayload) -> SpecificDepartureModel:
        return SpecificDepartureRepository.create(payload)

    @staticmethod
    def get(departure_id: uuid.UUID) -> SpecificDepartureModel:
        return SpecificDepartureRepository.get_one(departure_id)

    @staticmethod
    def update(departure_id: uuid.UUID, payload: UpdateSpecificDeparturePayload) -> SpecificDepartureModel:
        return SpecificDepartureRepository.update(departure_id, payload)

    @staticmethod
    def delete(departure_id: uuid.UUID):
        return SpecificDepartureRepository.delete(departure_id)
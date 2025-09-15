import uuid
from models.tour_departure import (
    CreateTourDeparturePayload,
    UpdateTourDeparturePayload,
    TourDepartureModel
)
from repositories.tour_departure import TourDepartureRepository


class TourDepartureService:
    @staticmethod
    def create(payload: CreateTourDeparturePayload) -> TourDepartureModel:
        return TourDepartureRepository.create(payload)

    @staticmethod
    def get(departure_id: uuid.UUID) -> TourDepartureModel:
        return TourDepartureRepository.get_one(departure_id)

    @staticmethod
    def update(departure_id: uuid.UUID, payload: UpdateTourDeparturePayload) -> TourDepartureModel:
        return TourDepartureRepository.update(departure_id, payload)

    @staticmethod
    def delete(departure_id: uuid.UUID):
        return TourDepartureRepository.delete(departure_id)
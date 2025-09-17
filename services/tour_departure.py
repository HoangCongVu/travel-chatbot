import uuid
from models.tour_departure import (
    CreateTourDeparture,
    UpdateTourDeparture,
    TourDepartureModel
)
from repositories.tour_departure import TourDepartureRepository


class TourDepartureService:
    @staticmethod
    def create(payload: CreateTourDeparture) -> TourDepartureModel:
        return TourDepartureRepository.create(payload)

    @staticmethod
    def get(departure_id: uuid.UUID) -> TourDepartureModel:
        return TourDepartureRepository.get_one(departure_id)

    @staticmethod
    def update(departure_id: uuid.UUID, payload: UpdateTourDeparture) -> TourDepartureModel:
        return TourDepartureRepository.update(departure_id, payload)

    @staticmethod
    def delete(departure_id: uuid.UUID):
        return TourDepartureRepository.delete(departure_id)
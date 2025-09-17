import uuid
from models.tour_destination import (
    CreateTourDestination,
    UpdateTourDestination,
    TourDestinationModel
)
from repositories.tour_destination import TourDestinationRepository


class TourDestinationService:
    @staticmethod
    def create(payload: CreateTourDestination) -> TourDestinationModel:
        return TourDestinationRepository.create(payload)

    @staticmethod
    def get(destination_id: uuid.UUID) -> TourDestinationModel:
        return TourDestinationRepository.get_one(destination_id)

    @staticmethod
    def update(destination_id: uuid.UUID, payload: UpdateTourDestination) -> TourDestinationModel:
        return TourDestinationRepository.update(destination_id, payload)

    @staticmethod
    def delete(destination_id: uuid.UUID):
        return TourDestinationRepository.delete(destination_id)
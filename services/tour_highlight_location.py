import uuid
from models.tour_highlight_location import (
    CreateTourHighlightLocation,
    UpdateTourHighlightLocation,
    TourHighlightLocationModel
)
from repositories.tour_highlight_location import TourHighlightLocationRepository


class TourHighlightLocationService:
    @staticmethod
    def create(payload: CreateTourHighlightLocation) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.create(payload)

    @staticmethod
    def get(location_id: uuid.UUID) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.get_one(location_id)

    @staticmethod
    def update(location_id: uuid.UUID, payload: UpdateTourHighlightLocation) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.update(location_id, payload)

    @staticmethod
    def delete(location_id: uuid.UUID):
        return TourHighlightLocationRepository.delete(location_id)
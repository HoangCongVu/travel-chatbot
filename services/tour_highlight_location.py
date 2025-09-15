import uuid
from models.tour_highlight_location import (
    CreateTourHighlightLocationPayload,
    UpdateTourHighlightLocationPayload,
    TourHighlightLocationModel
)
from repositories.tour_highlight_location import TourHighlightLocationRepository


class TourHighlightLocationService:
    @staticmethod
    def create(payload: CreateTourHighlightLocationPayload) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.create(payload)

    @staticmethod
    def get(location_id: uuid.UUID) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.get_one(location_id)

    @staticmethod
    def update(location_id: uuid.UUID, payload: UpdateTourHighlightLocationPayload) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.update(location_id, payload)

    @staticmethod
    def delete(location_id: uuid.UUID):
        return TourHighlightLocationRepository.delete(location_id)
import uuid
from models.tour_highlight_location import CreateTourHighlightLocation, UpdateTourHighlightLocation, TourHighlightLocationModel
from repositories.tour_highlight_location import TourHighlightLocationRepository


class TourHighlightLocationService:
    @staticmethod
    def create(payload: CreateTourHighlightLocation) -> TourHighlightLocationModel:
        return TourHighlightLocationRepository.create(payload)
    
    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: UpdateTourHighlightLocation) -> list[TourHighlightLocationModel]:
        return TourHighlightLocationRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(location_id: uuid.UUID):
        return TourHighlightLocationRepository.delete(location_id)
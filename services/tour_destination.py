import uuid
from models.tour_destination import CreateTourDestination, UpdateTourDestination, TourDestinationModel
from repositories.tour_destination import TourDestinationRepository


class TourDestinationService:
    @staticmethod
    def create(payload: CreateTourDestination) -> TourDestinationModel:
        return TourDestinationRepository.create(payload)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: UpdateTourDestination) -> list[TourDestinationModel]:
        return TourDestinationRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(destination_id: uuid.UUID):
        return TourDestinationRepository.delete(destination_id)
    
    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        """
        Tìm kiếm tour destination theo text (semantic search).
        """
        return TourDestinationRepository.search_by_text(query=query, limit=limit)
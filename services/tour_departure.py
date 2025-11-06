import uuid
from models.tour_departure import CreateTourDeparture, UpdateTourDeparture, TourDepartureModel
from repositories.tour_departure import TourDepartureRepository


class TourDepartureService:
    @staticmethod
    def create(payload: CreateTourDeparture) -> TourDepartureModel:
        return TourDepartureRepository.create(payload)
    
    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: UpdateTourDeparture) -> list[TourDepartureModel]:
        return TourDepartureRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(departure_id: uuid.UUID):
        return TourDepartureRepository.delete(departure_id)

    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        """
        Tìm kiếm tour departure theo text (semantic search).
        """
        return TourDepartureRepository.search_by_text(query=query, limit=limit)

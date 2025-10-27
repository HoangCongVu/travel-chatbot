import uuid
from models.tour import TourCreateModel, TourUpdateModel, TourModel
from repositories.tour import TourRepository
from datetime import date


class TourService:
    @staticmethod
    def create(payload: TourCreateModel) -> TourModel:
        return TourRepository.create(payload)

    @staticmethod
    def get(tour_id: uuid.UUID) -> TourModel | None:
        return TourRepository.get(tour_id)

    @staticmethod
    def update(tour_id: uuid.UUID, payload: TourUpdateModel) -> TourModel | None:
        return TourRepository.update(tour_id, payload)

    @staticmethod
    def delete(tour_id: uuid.UUID) -> bool:
        return TourRepository.delete(tour_id)
    
    @staticmethod
    def delete_with_related(tour_id: uuid.UUID) -> bool:
        """
        Xóa tour và tất cả các bảng liên quan.
        """
        return TourRepository.delete_with_related(tour_id)

    @staticmethod
    def get_all() -> list[TourModel]:
        return TourRepository.get_all()

    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        """
        Tìm kiếm tour theo text (semantic search).
        """
        return TourRepository.search_by_text(query=query, limit=limit)

    @staticmethod
    def tour_by_date(target_date: date):
        """
        Tìm kiếm tour theo ngày (dựa vào specific_departures / recurring_schedules / price_by_dates).
        """
        return TourRepository.tour_by_date(target_date)
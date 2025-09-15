import uuid
from models.tour import TourCreateModel, TourUpdateModel, TourModel
from repositories.tour import TourRepository


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
    def get_all() -> list[TourModel]:
        return TourRepository.get_all()

import uuid
from models.departure_schedule import CreateDepartureSchedule, UpdateDepartureSchedule, DepartureScheduleModel
from repositories.departure_schedule import DepartureScheduleRepository


class DepartureScheduleService:
    @staticmethod
    def create(payload: CreateDepartureSchedule) -> DepartureScheduleModel:
        return DepartureScheduleRepository.create(payload)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, payload: UpdateDepartureSchedule) -> list[DepartureScheduleModel]:
        return DepartureScheduleRepository.update_by_tour_id(tour_id, payload)

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        return DepartureScheduleRepository.delete(schedule_id)
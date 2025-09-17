import uuid
from models.departure_schedule import (
    CreateDepartureSchedule,
    UpdateDepartureSchedule,
    DepartureScheduleModel
)
from repositories.departure_schedule import DepartureScheduleRepository


class DepartureScheduleService:
    @staticmethod
    def create(payload: CreateDepartureSchedule) -> DepartureScheduleModel:
        return DepartureScheduleRepository.create(payload)

    @staticmethod
    def get(schedule_id: uuid.UUID) -> DepartureScheduleModel:
        return DepartureScheduleRepository.get_one(schedule_id)

    @staticmethod
    def update(schedule_id: uuid.UUID, payload: UpdateDepartureSchedule) -> DepartureScheduleModel:
        return DepartureScheduleRepository.update(schedule_id, payload)

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        return DepartureScheduleRepository.delete(schedule_id)
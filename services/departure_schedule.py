import uuid
from models.departure_schedule import (
    CreateDepartureSchedulePayload,
    UpdateDepartureSchedulePayload,
    DepartureScheduleModel
)
from repositories.departure_schedule import DepartureScheduleRepository


class DepartureScheduleService:
    @staticmethod
    def create(payload: CreateDepartureSchedulePayload) -> DepartureScheduleModel:
        return DepartureScheduleRepository.create(payload)

    @staticmethod
    def get(schedule_id: uuid.UUID) -> DepartureScheduleModel:
        return DepartureScheduleRepository.get_one(schedule_id)

    @staticmethod
    def update(schedule_id: uuid.UUID, payload: UpdateDepartureSchedulePayload) -> DepartureScheduleModel:
        return DepartureScheduleRepository.update(schedule_id, payload)

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        return DepartureScheduleRepository.delete(schedule_id)
import uuid
from models.recurring_schedule import (
    CreateRecurringSchedulePayload,
    UpdateRecurringSchedulePayload,
    RecurringScheduleModel
)
from repositories.recurring_schedule import RecurringScheduleRepository

class RecurringScheduleService:
    @staticmethod
    def create(payload: CreateRecurringSchedulePayload) -> RecurringScheduleModel:
        return RecurringScheduleRepository.create(payload)

    @staticmethod
    def get(schedule_id: uuid.UUID) -> RecurringScheduleModel:
        return RecurringScheduleRepository.get_one(schedule_id)

    @staticmethod
    def update(schedule_id: uuid.UUID, payload: UpdateRecurringSchedulePayload) -> RecurringScheduleModel:
        return RecurringScheduleRepository.update(schedule_id, payload)

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        return RecurringScheduleRepository.delete(schedule_id)
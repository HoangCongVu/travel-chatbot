import uuid
from db import Session
from models.recurring_schedule import (
    RecurringSchedule,
    CreateRecurringSchedule,
    UpdateRecurringSchedule,
    RecurringScheduleModel
)

class RecurringScheduleRepository:
    @staticmethod
    def create(payload: CreateRecurringSchedule) -> RecurringScheduleModel:
        with Session() as session:
            schedule = RecurringSchedule(**payload.model_dump())
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            return RecurringScheduleModel.model_validate(schedule)

    @staticmethod
    def get_one(schedule_id: uuid.UUID) -> RecurringScheduleModel:
        with Session() as session:
            schedule = session.get(RecurringSchedule, schedule_id)
            if schedule is None:
                raise ValueError(f"Recurring schedule with ID {schedule_id} not found.")
            return RecurringScheduleModel.model_validate(schedule)

    @staticmethod
    def update(schedule_id: uuid.UUID, data: UpdateRecurringSchedule) -> RecurringScheduleModel:
        with Session() as session:
            schedule = session.get(RecurringSchedule, schedule_id)
            if schedule is None:
                raise ValueError(f"Recurring schedule with ID {schedule_id} not found.")
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(schedule, field, value)
            session.commit()
            session.refresh(schedule)
            return RecurringScheduleModel.model_validate(schedule)

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        with Session() as session:
            schedule = session.get(RecurringSchedule, schedule_id)
            if schedule is None:
                raise ValueError(f"Recurring schedule with ID {schedule_id} not found.")
            session.delete(schedule)
            session.commit()
import uuid
from db import Session
from models.departure_schedule import (
    DepartureSchedule,
    CreateDepartureSchedulePayload,
    UpdateDepartureSchedulePayload,
    DepartureScheduleModel
)


class DepartureScheduleRepository:
    @staticmethod
    def create(payload: CreateDepartureSchedulePayload) -> DepartureScheduleModel:
        with Session() as session:
            schedule = DepartureSchedule(**payload.model_dump())
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            return DepartureScheduleModel.model_validate(schedule)

    @staticmethod
    def get_one(schedule_id: uuid.UUID) -> DepartureScheduleModel:
        with Session() as session:
            schedule = session.get(DepartureSchedule, schedule_id)
            return DepartureScheduleModel.model_validate(schedule)

    @staticmethod
    def update(schedule_id: uuid.UUID, data: UpdateDepartureSchedulePayload) -> DepartureScheduleModel:
        with Session() as session:
            schedule = session.get(DepartureSchedule, schedule_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(schedule, field, value)
            session.commit()
            session.refresh(schedule)
            return DepartureScheduleModel.model_validate(schedule)

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        with Session() as session:
            schedule = session.get(DepartureSchedule, schedule_id)
            session.delete(schedule)
            session.commit()
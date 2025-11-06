import uuid
from db import Session
from models.departure_schedule import DepartureSchedule, CreateDepartureSchedule, UpdateDepartureSchedule, DepartureScheduleModel


class DepartureScheduleRepository:
    @staticmethod
    def create(payload: CreateDepartureSchedule) -> DepartureScheduleModel:
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
    def update(schedule_id: uuid.UUID, data: UpdateDepartureSchedule) -> DepartureScheduleModel:
        with Session() as session:
            schedule = session.get(DepartureSchedule, schedule_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(schedule, field, value)
            session.commit()
            session.refresh(schedule)
            return DepartureScheduleModel.model_validate(schedule)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, data: UpdateDepartureSchedule) -> list[DepartureScheduleModel]:
        with Session() as session:
            schedules = session.query(DepartureSchedule).filter(DepartureSchedule.tour_id == tour_id).all()
            if not schedules:
                return []
            
            updated_schedules = []
            for schedule in schedules:
                for field, value in data.model_dump(exclude_unset=True).items():
                    setattr(schedule, field, value)
                updated_schedules.append(DepartureScheduleModel.model_validate(schedule))
            
            session.commit()
            return updated_schedules

    @staticmethod
    def delete(schedule_id: uuid.UUID):
        with Session() as session:
            schedule = session.get(DepartureSchedule, schedule_id)
            session.delete(schedule)
            session.commit()
    
    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[DepartureScheduleModel]:
        with Session() as session:
            schedules = session.query(DepartureSchedule).filter(DepartureSchedule.tour_id == tour_id).all()
            return [DepartureScheduleModel.model_validate(s) for s in schedules]

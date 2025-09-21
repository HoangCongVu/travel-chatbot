import uuid
from db import Session
from datetime import datetime, timezone
from models.specific_departure import SpecificDeparture, CreateSpecificDeparture, UpdateSpecificDeparture, SpecificDepartureModel
from models.departure_schedule import DepartureSchedule


class SpecificDepartureRepository:
    @staticmethod
    def create(payload: CreateSpecificDeparture) -> SpecificDepartureModel:
        with Session() as session:
            departure = SpecificDeparture(**payload.model_dump())
            session.add(departure)
            session.commit()
            session.refresh(departure)
            return SpecificDepartureModel.model_validate(departure)

    @staticmethod
    def get_one(departure_id: uuid.UUID) -> SpecificDepartureModel:
        with Session() as session:
            departure = session.get(SpecificDeparture, departure_id)
            return SpecificDepartureModel.model_validate(departure)

    @staticmethod
    def update(departure_id: uuid.UUID, data: UpdateSpecificDeparture) -> SpecificDepartureModel:
        with Session() as session:
            departure = session.get(SpecificDeparture, departure_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(departure, field, value)
            session.commit()
            session.refresh(departure)
            return SpecificDepartureModel.model_validate(departure)

    @staticmethod
    def delete(departure_id: uuid.UUID):
        with Session() as session:
            departure = session.get(SpecificDeparture, departure_id)
            session.delete(departure)
            session.commit()
            return {"message": "Specific departure deleted successfully"}

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[SpecificDepartureModel]:
        with Session() as session:
            departures = (
                session.query(SpecificDeparture)
                .join(DepartureSchedule, SpecificDeparture.schedule_id == DepartureSchedule.id)
                .filter(DepartureSchedule.tour_id == tour_id)
                .all()
            )
            return [SpecificDepartureModel.model_validate(d) for d in departures]

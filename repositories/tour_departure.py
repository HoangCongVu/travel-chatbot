import uuid
from db import Session
from datetime import datetime, timezone
from models.tour_departure import (
    TourDeparture,
    CreateTourDeparture,
    UpdateTourDeparture,
    TourDepartureModel
)


class TourDepartureRepository:
    @staticmethod
    def create(payload: CreateTourDeparture) -> TourDepartureModel:
        with Session() as session:
            departure = TourDeparture(id=uuid.uuid4(), **payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(departure)
            session.commit()
            session.refresh(departure)
            return TourDepartureModel.model_validate(departure)

    @staticmethod
    def get_one(departure_id: uuid.UUID) -> TourDepartureModel:
        with Session() as session:
            departure = session.get(TourDeparture, departure_id)
            return TourDepartureModel.model_validate(departure)

    @staticmethod
    def update(departure_id: uuid.UUID, data: UpdateTourDeparture) -> TourDepartureModel:
        with Session() as session:
            departure = session.get(TourDeparture, departure_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(departure, field, value)
            session.commit()
            session.refresh(departure)
            return TourDepartureModel.model_validate(departure)

    @staticmethod
    def delete(departure_id: uuid.UUID):
        with Session() as session:
            departure = session.get(TourDeparture, departure_id)
            session.delete(departure)
            session.commit()
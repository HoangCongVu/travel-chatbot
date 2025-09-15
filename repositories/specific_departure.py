import uuid
from db import Session
from datetime import datetime, timezone
from models.specific_departure import (
    SpecificDeparture,
    CreateSpecificDeparturePayload,
    UpdateSpecificDeparturePayload,
    SpecificDepartureModel
)


class SpecificDepartureRepository:
    @staticmethod
    def create(payload: CreateSpecificDeparturePayload) -> SpecificDepartureModel:
        with Session() as session:
            departure = SpecificDeparture(**payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
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
    def update(departure_id: uuid.UUID, data: UpdateSpecificDeparturePayload) -> SpecificDepartureModel:
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
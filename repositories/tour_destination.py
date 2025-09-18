import uuid
from db import Session
import numpy as np
from datetime import datetime, timezone
from models.tour_destination import (
    TourDestination,
    CreateTourDestination,
    UpdateTourDestination,
    TourDestinationModel
)

class TourDestinationRepository:
    @staticmethod
    def create(payload: CreateTourDestination) -> TourDestinationModel:
        with Session() as session:
            destination = TourDestination(id=uuid.uuid4(), **payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(destination)
            session.commit()
            session.refresh(destination)
            return TourDestinationModel.model_validate(destination)

    @staticmethod
    def get_one(destination_id: uuid.UUID) -> TourDestinationModel:
        with Session() as session:
            destination = session.get(TourDestination, destination_id)
            return TourDestinationModel.model_validate(destination)

    @staticmethod
    def update(destination_id: uuid.UUID, data: UpdateTourDestination) -> TourDestinationModel:
        with Session() as session:
            destination = session.get(TourDestination, destination_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(destination, field, value)
            session.commit()
            session.refresh(destination)
            return TourDestinationModel.model_validate(destination)

    @staticmethod
    def delete(destination_id: uuid.UUID):
        with Session() as session:
            destination = session.get(TourDestination, destination_id)
            session.delete(destination)
            session.commit()
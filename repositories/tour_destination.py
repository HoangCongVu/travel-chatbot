import uuid
from db import Session
import numpy as np
from datetime import datetime, timezone
from models.tour_destination import (
    TourDestination,
    CreateTourDestinationPayload,
    UpdateTourDestinationPayload,
    TourDestinationModel
)

class TourDestinationRepository:
    @staticmethod
    def create(payload: CreateTourDestinationPayload) -> TourDestinationModel:
        with Session() as session:
            # destination = TourDestination(**payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc), destination_embedding_vector=np.zeros(1536))
            destination = TourDestination(**payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(destination)
            session.commit()
            session.refresh(destination)
            return TourDestinationModel.model_validate(destination.__dict__)

    @staticmethod
    def get_one(destination_id: uuid.UUID) -> TourDestinationModel:
        with Session() as session:
            destination = session.get(TourDestination, destination_id)
            return TourDestinationModel.model_validate(destination.__dict__)

    @staticmethod
    def update(destination_id: uuid.UUID, data: UpdateTourDestinationPayload) -> TourDestinationModel:
        with Session() as session:
            destination = session.get(TourDestination, destination_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(destination, field, value)
            session.commit()
            session.refresh(destination)
            return TourDestinationModel.model_validate(destination.__dict__)

    @staticmethod
    def delete(destination_id: uuid.UUID):
        with Session() as session:
            destination = session.get(TourDestination, destination_id)
            session.delete(destination)
            session.commit()
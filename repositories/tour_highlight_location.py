import uuid
from db import Session
from datetime import datetime, timezone
from models.tour_highlight_location import (
    TourHighlightLocation,
    CreateTourHighlightLocation,
    UpdateTourHighlightLocation,
    TourHighlightLocationModel
)


class TourHighlightLocationRepository:
    @staticmethod
    def create(payload: CreateTourHighlightLocation) -> TourHighlightLocationModel:
        with Session() as session:
            location = TourHighlightLocation(id=uuid.uuid4(), **payload.model_dump(), created_at=datetime.now(tz=timezone.utc), updated_at=datetime.now(tz=timezone.utc))
            session.add(location)
            session.commit()
            session.refresh(location)
            return TourHighlightLocationModel.model_validate(location)

    @staticmethod
    def get_one(location_id: uuid.UUID) -> TourHighlightLocationModel:
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            return TourHighlightLocationModel.model_validate(location)

    @staticmethod
    def update(location_id: uuid.UUID, data: UpdateTourHighlightLocation) -> TourHighlightLocationModel:
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(location, field, value)
            session.commit()
            session.refresh(location)
            return TourHighlightLocationModel.model_validate(location)

    @staticmethod
    def delete(location_id: uuid.UUID):
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            session.delete(location)
            session.commit()
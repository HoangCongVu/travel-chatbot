import uuid
from db import Session
from models.tour_highlight_location import (
    TourHighlightLocation,
    CreateTourHighlightLocationPayload,
    UpdateTourHighlightLocationPayload,
    TourHighlightLocationModel
)


class TourHighlightLocationRepository:
    @staticmethod
    def create(payload: CreateTourHighlightLocationPayload) -> TourHighlightLocationModel:
        with Session() as session:
            location = TourHighlightLocation(**payload.model_dump())
            session.add(location)
            session.commit()
            session.refresh(location)
            return TourHighlightLocationModel.model_validate(location.__dict__)

    @staticmethod
    def get_one(location_id: uuid.UUID) -> TourHighlightLocationModel:
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            return TourHighlightLocationModel.model_validate(location.__dict__)

    @staticmethod
    def update(location_id: uuid.UUID, data: UpdateTourHighlightLocationPayload) -> TourHighlightLocationModel:
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(location, field, value)
            session.commit()
            session.refresh(location)
            return TourHighlightLocationModel.model_validate(location.__dict__)

    @staticmethod
    def delete(location_id: uuid.UUID):
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            session.delete(location)
            session.commit()
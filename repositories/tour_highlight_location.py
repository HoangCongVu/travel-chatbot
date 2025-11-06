import uuid
from db import Session
from datetime import datetime, timezone
from models.tour_highlight_location import TourHighlightLocation, CreateTourHighlightLocation, UpdateTourHighlightLocation, TourHighlightLocationModel


class TourHighlightLocationRepository:
    @staticmethod
    def create(payload: CreateTourHighlightLocation) -> TourHighlightLocationModel:
        with Session() as session:
            location = TourHighlightLocation(id=uuid.uuid4(), **payload.model_dump())
            session.add(location)
            session.commit()
            session.refresh(location)
            return TourHighlightLocationModel.model_validate(location)

    @staticmethod
    def update_by_tour_id(tour_id: uuid.UUID, data: UpdateTourHighlightLocation) -> list[TourHighlightLocationModel]:
        with Session() as session:
            locations = session.query(TourHighlightLocation).filter(TourHighlightLocation.tour_id == tour_id).all()
            if not locations:
                return []
            
            updated_locations = []
            for location in locations:
                for field, value in data.model_dump(exclude_unset=True).items():
                    setattr(location, field, value)
                updated_locations.append(TourHighlightLocationModel.model_validate(location))
            
            session.commit()
            return updated_locations

    @staticmethod
    def delete(location_id: uuid.UUID):
        with Session() as session:
            location = session.get(TourHighlightLocation, location_id)
            session.delete(location)
            session.commit()
    
    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[TourHighlightLocationModel]:
        with Session() as session:
            destinations = (
                session.query(TourHighlightLocation)
                .filter(TourHighlightLocation.tour_id == tour_id)
                .all()
            )
            return [TourHighlightLocationModel.model_validate(d) for d in destinations]

from db import Session
from models.tour_type import (
    TourTypeTable,
    CreateTourType,
    UpdateTourType,
    TourTypeModel
)
from datetime import datetime, timezone


class TourTypeRepository:
    @staticmethod
    def create(payload: CreateTourType) -> TourTypeModel:
        with Session() as session:
            tour_type = TourTypeTable(**payload.model_dump())
            session.add(tour_type)
            session.commit()
            session.refresh(tour_type)
            return TourTypeModel.model_validate(tour_type)

    @staticmethod
    def get_one(type_id: int) -> TourTypeModel:
        with Session() as session:
            tour_type = session.get(TourTypeTable, type_id)
            return TourTypeModel.model_validate(tour_type)

    @staticmethod
    def update(type_id: int, data: UpdateTourType) -> TourTypeModel:
        with Session() as session:
            tour_type = session.get(TourTypeTable, type_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(tour_type, field, value)
            session.commit()
            session.refresh(tour_type)
            return TourTypeModel.model_validate(tour_type)

    @staticmethod
    def delete(type_id: int):
        with Session() as session:
            tour_type = session.get(TourTypeTable, type_id)
            session.delete(tour_type)
            session.commit()
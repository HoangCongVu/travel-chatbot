# repositories/tour_type.py
from db import Session
from models.tour_type import (
    TourTypeTable,
    CreateTourType,
    UpdateTourType,
    TourTypeModel
)


class TourTypeRepository:
    @staticmethod
    def create(payload: CreateTourType) -> TourTypeModel:
        with Session() as session:
            # exclude_unset tránh đưa id=None hay field không cần thiết
            data = payload.model_dump(exclude_unset=True)
            tour_type = TourTypeTable(**data)
            session.add(tour_type)
            session.commit()
            session.refresh(tour_type)
            return TourTypeModel.model_validate(tour_type)

    @staticmethod
    def get_one(type_id: int) -> TourTypeModel | None:
        with Session() as session:
            tour_type = session.get(TourTypeTable, type_id)
            # chỉ validate nếu có kết quả, nếu không thì trả về None
            return TourTypeModel.model_validate(tour_type) if tour_type else None

    @staticmethod
    def get_by_name(type_name: str) -> TourTypeModel | None:
        with Session() as session:
            tour_type = session.query(TourTypeTable).filter(
                TourTypeTable.type_name == type_name
            ).first()
            return TourTypeModel.model_validate(tour_type) if tour_type else None

    @staticmethod
    def update(type_id: int, data: UpdateTourType) -> TourTypeModel | None:
        with Session() as session:
            tour_type = session.get(TourTypeTable, type_id)
            if not tour_type:
                return None
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(tour_type, field, value)
            session.commit()
            session.refresh(tour_type)
            return TourTypeModel.model_validate(tour_type)

    @staticmethod
    def delete(type_id: int) -> bool:
        with Session() as session:
            tour_type = session.get(TourTypeTable, type_id)
            if not tour_type:
                return False
            session.delete(tour_type)
            session.commit()
            return True

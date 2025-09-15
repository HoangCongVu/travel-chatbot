import uuid
from db import Session
from models.tour import TourTable, TourCreateModel, TourUpdateModel, TourModel
# from controllers.embedding import generate_embedding


class TourRepository:
    @staticmethod
    def create(payload: TourCreateModel) -> TourModel:
        with Session() as session:
            tour = TourTable(
                **payload.model_dump(),
                id=uuid.uuid4(),
                # tours_name_embedding_vector=generate_embedding(payload.tour_name),
            )
            session.add(tour)
            session.commit()
            session.refresh(tour)
            return TourModel.model_validate(tour)

    @staticmethod
    def get(tour_id: uuid.UUID) -> TourModel | None:
        with Session() as session:
            tour = session.query(TourTable).filter(TourTable.id == tour_id).first()
            return TourModel.model_validate(tour) if tour else None

    @staticmethod
    def update(tour_id: uuid.UUID, payload: TourUpdateModel) -> TourModel | None:
        with Session() as session:
            tour = session.query(TourTable).filter(TourTable.id == tour_id).first()
            if not tour:
                return None
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(tour, key, value)
            session.commit()
            session.refresh(tour)
            return TourModel.model_validate(tour)

    @staticmethod
    def delete(tour_id: uuid.UUID) -> bool:
        with Session() as session:
            tour = session.query(TourTable).filter(TourTable.id == tour_id).first()
            if not tour:
                return False
            session.delete(tour)
            session.commit()
            return True

    @staticmethod
    def get_all() -> list[TourModel]:
        with Session() as session:
            tours = session.query(TourTable).all()
            return [TourModel.model_validate(t) for t in tours][::-1]

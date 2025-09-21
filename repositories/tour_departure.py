import uuid
from db import Session
from datetime import datetime, timezone
from models.tour_departure import TourDeparture, CreateTourDeparture, UpdateTourDeparture, TourDepartureModel, SearchTourDeparture
from utils.embedding import generate_embedding
from pgvector.sqlalchemy import Vector
from utils.embedding import generate_embedding 
import sqlalchemy as sa

class TourDepartureRepository:
    @staticmethod
    def create(payload: CreateTourDeparture) -> TourDepartureModel:
        with Session() as session:
            departure = TourDeparture(id=uuid.uuid4(), **payload.model_dump(), tour_departure_embedding_vector=generate_embedding(payload.departure_name))
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

    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        query_vector = generate_embedding(query)
        with Session() as session:
            rows = session.execute(
                sa.text("""
                    SELECT id, tour_id, departure_name
                    FROM tour_departures
                    ORDER BY tour_departure_embedding_vector <-> (:query_vector)::vector
                    LIMIT :limit
                """),
                {"query_vector": query_vector, "limit": limit}
            ).fetchall()

            return [SearchTourDeparture(**row._mapping) for row in rows]

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[TourDepartureModel]:
        with Session() as session:
            departures = (
                session.query(TourDeparture)
                .filter(TourDeparture.tour_id == tour_id)
                .all()
            )
            return [TourDepartureModel.model_validate(d) for d in departures]

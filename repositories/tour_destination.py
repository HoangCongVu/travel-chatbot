import uuid
from db import Session
import numpy as np
from datetime import datetime, timezone
from models.tour_destination import TourDestination, CreateTourDestination, UpdateTourDestination, TourDestinationModel, SearchTourDestination
from utils.embedding import generate_embedding
from pgvector.sqlalchemy import Vector
from utils.embedding import generate_embedding
import sqlalchemy as sa 

class TourDestinationRepository:
    @staticmethod
    def create(payload: CreateTourDestination) -> TourDestinationModel:
        with Session() as session:
            destination = TourDestination(id=uuid.uuid4(), **payload.model_dump(), tour_destination_embedding_vector=generate_embedding(payload.destination_name))
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
            return {"message": "Tour destination deleted successfully"}

    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        query_vector = generate_embedding(query)
        with Session() as session:
            rows = session.execute(
                sa.text("""
                    SELECT id, tour_id, destination_name
                    FROM tour_destinations
                    ORDER BY tour_destination_embedding_vector <-> (:query_vector)::vector
                    LIMIT :limit
                """),
                {"query_vector": query_vector, "limit": limit}
            ).fetchall()

            return [SearchTourDestination(**row._mapping) for row in rows]
    

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID) -> list[TourDestinationModel]:
        with Session() as session:
            destinations = (
                session.query(TourDestination)
                .filter(TourDestination.tour_id == tour_id)
                .all()
            )
            return [TourDestinationModel.model_validate(d) for d in destinations]
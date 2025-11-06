import uuid
from db import Session
from utils.embedding import generate_embedding
from models.tour import TourTable, TourCreateModel, TourUpdateModel, TourModel, SearchTour
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa
from sqlalchemy import func, DateTime, select
from models.departure_schedule import DepartureSchedule
from models.specific_departure import SpecificDeparture
from models.recurring_schedule import RecurringSchedule
from models.price_by_date import PriceByDate
from models.visa_price import VisaPriceTable
from models.tour_highlight_location import TourHighlightLocation
from models.tour_destination import TourDestination
from models.tour_departure import TourDeparture
from models.price_by_package import PriceByPackage

class TourRepository:
    @staticmethod
    def create(payload: TourCreateModel) -> TourModel:
        with Session() as session:
            tour = TourTable(**payload.model_dump(),id=uuid.uuid4(),
            tour_embedding_vector=generate_embedding(payload.tour_name))
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
    def delete_with_related(tour_id: uuid.UUID) -> bool:
        """
        Xóa tour và tất cả các bảng liên quan:
        - departure_schedules (và cascade: specific_departures, recurring_schedules)
        - visa_prices
        - tour_highlight_locations
        - tour_destinations
        - tour_departures
        - price_by_packages
        - price_by_dates
        """
        with Session() as session:
            tour = session.query(TourTable).filter(TourTable.id == tour_id).first()
            if not tour:
                return False
            
            # Lấy danh sách departure_schedules của tour
            departure_schedules = session.query(DepartureSchedule).filter(
                DepartureSchedule.tour_id == tour_id
            ).all()
            
            schedule_ids = [schedule.id for schedule in departure_schedules]
            
            # Xóa specific_departures và recurring_schedules liên quan đến departure_schedules
            if schedule_ids:
                session.query(SpecificDeparture).filter(
                    SpecificDeparture.schedule_id.in_(schedule_ids)
                ).delete(synchronize_session=False)
                
                session.query(RecurringSchedule).filter(
                    RecurringSchedule.schedule_id.in_(schedule_ids)
                ).delete(synchronize_session=False)
            
            # Xóa departure_schedules
            session.query(DepartureSchedule).filter(
                DepartureSchedule.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            # Xóa các bảng khác liên quan trực tiếp đến tour_id
            session.query(VisaPriceTable).filter(
                VisaPriceTable.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            session.query(TourHighlightLocation).filter(
                TourHighlightLocation.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            session.query(TourDestination).filter(
                TourDestination.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            session.query(TourDeparture).filter(
                TourDeparture.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            session.query(PriceByPackage).filter(
                PriceByPackage.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            session.query(PriceByDate).filter(
                PriceByDate.tour_id == tour_id
            ).delete(synchronize_session=False)
            
            # Cuối cùng xóa tour
            session.delete(tour)
            session.commit()
            return True

    @staticmethod
    def get_all() -> list[TourModel]:
        with Session() as session:
            tours = session.query(TourTable).all()
            return [TourModel.model_validate(t) for t in tours][::-1]
    
    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        query_vector = generate_embedding(query)
        with Session() as session:
            rows = session.execute(
                sa.text("""
                    SELECT id, tour_name, days, description, highlight, itinerary_url, image_url, promotion_info, price_type
                    FROM tours
                    ORDER BY tour_embedding_vector <-> (:query_vector)::vector
                    LIMIT :limit
                """),
                {"query_vector": query_vector, "limit": limit}
            ).fetchall()

            return [SearchTour(**row._mapping) for row in rows]

    @staticmethod
    def tour_by_date(target_date):
        with Session() as session:
            # SpecificDeparture -> DepartureSchedule -> Tour
            q1 = (
                session.query(DepartureSchedule.tour_id)
                .join(SpecificDeparture, SpecificDeparture.schedule_id == DepartureSchedule.id)
                .filter(SpecificDeparture.date == target_date)
            )

            # RecurringSchedule -> DepartureSchedule -> Tour
            q2 = (
                session.query(DepartureSchedule.tour_id)
                .join(RecurringSchedule, RecurringSchedule.schedule_id == DepartureSchedule.id)
                .filter(
                    RecurringSchedule.start_date <= target_date,
                    RecurringSchedule.end_date >= target_date,
                    func.extract("isodow", target_date) == func.any(RecurringSchedule.weekdays)
                )
            )

            # PriceByDate -> Tour
            q3 = (
                session.query(PriceByDate.tour_id)
                .filter(PriceByDate.date == target_date)
            )

            # union kết quả
            tour_ids = q1.union(q2, q3).distinct().all()

            return [tid[0] for tid in tour_ids]

    @staticmethod
    def search_by_tour_type(tour_type_id: int) -> list[TourModel]:
        """
        Tìm kiếm tour theo tour_type_id
        """
        with Session() as session:
            tours = session.query(TourTable).filter(TourTable.tour_type_id == tour_type_id).all()
            return [TourModel.model_validate(t) for t in tours][::-1]  # Đảo ngược để lấy tour mới nhất trước


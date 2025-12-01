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

    @staticmethod
    def search_tour_chat(destination: str = None, min_price: float = None, max_price: float = None, target_date = None, limit: int = 5):
        """
        Tìm kiếm tour với nhiều điều kiện kết hợp:
        - destination: Tên địa điểm đích (tìm kiếm trong tour_destinations)
        - min_price, max_price: Khoảng giá (tìm trong price_by_packages hoặc price_by_dates)
        - target_date: Ngày khởi hành (tìm trong specific_departures hoặc recurring_schedules)
        - limit: Giới hạn số lượng kết quả
        
        Returns:
            List các tour_id thỏa mãn điều kiện
        """
        from datetime import date as date_type
        
        with Session() as session:
            # Bắt đầu với query cơ bản từ bảng tours
            query = session.query(TourTable.id).distinct()
            
            # Điều kiện 1: Lọc theo destination
            if destination:
                query = query.join(
                    TourDestination, 
                    TourTable.id == TourDestination.tour_id
                ).filter(
                    TourDestination.destination_name.ilike(f"%{destination}%")
                )
            
            # Điều kiện 2: Lọc theo khoảng giá
            if min_price is not None or max_price is not None:
                # Subquery cho price_by_packages
                price_package_subquery = (
                    session.query(PriceByPackage.tour_id)
                    .filter(PriceByPackage.tour_id == TourTable.id)
                )
                if min_price is not None:
                    price_package_subquery = price_package_subquery.filter(PriceByPackage.price >= min_price)
                if max_price is not None:
                    price_package_subquery = price_package_subquery.filter(PriceByPackage.price <= max_price)
                
                # Subquery cho price_by_dates
                price_date_subquery = (
                    session.query(PriceByDate.tour_id)
                    .filter(PriceByDate.tour_id == TourTable.id)
                )
                if min_price is not None:
                    price_date_subquery = price_date_subquery.filter(PriceByDate.price >= min_price)
                if max_price is not None:
                    price_date_subquery = price_date_subquery.filter(PriceByDate.price <= max_price)
                
                # Kết hợp điều kiện: tour phải có giá trong khoảng (từ một trong hai bảng)
                query = query.filter(
                    sa.or_(
                        price_package_subquery.exists(),
                        price_date_subquery.exists()
                    )
                )
            
            # Điều kiện 3: Lọc theo ngày khởi hành
            if target_date:
                if isinstance(target_date, str):
                    target_date = date_type.fromisoformat(target_date)
                
                # Subquery 1: Specific departures (Ngày khởi hành cụ thể)
                specific_subquery = (
                    session.query(DepartureSchedule.tour_id)
                    .join(SpecificDeparture, SpecificDeparture.schedule_id == DepartureSchedule.id)
                    .filter(
                        DepartureSchedule.tour_id == TourTable.id,
                        SpecificDeparture.date == target_date
                    )
                )
                
                # Subquery 2: Recurring schedules - Tìm theo NGÀY BẮT ĐẦU (start_date)
                recurring_subquery = (
                    session.query(DepartureSchedule.tour_id)
                    .join(RecurringSchedule, RecurringSchedule.schedule_id == DepartureSchedule.id)
                    .filter(
                        DepartureSchedule.tour_id == TourTable.id,
                        RecurringSchedule.start_date == target_date  # Chỉ tìm tour BẮT ĐẦU vào ngày này
                    )
                )
                
                # Kết hợp điều kiện: tour khởi hành vào ngày đó
                query = query.filter(
                    sa.or_(
                        specific_subquery.exists(),
                        recurring_subquery.exists()
                    )
                )
            
            # Giới hạn số lượng kết quả
            tour_ids = query.limit(limit).all()
            
            return [tid[0] for tid in tour_ids]

    @staticmethod
    def search_tour_by_fields(tour_type_id: int = None, destination: str = None, departure: str = None, target_date = None, limit: int = 5):
        """
        Tìm kiếm tour với các điều kiện:
        - tour_type_id: ID loại tour
        - destination: Tên địa điểm đích (tìm kiếm bằng embedding trong tour_destinations)
        - departure: Tên điểm khởi hành (tìm kiếm bằng embedding trong tour_departures)
        - target_date: Ngày khởi hành (tìm trong specific_departures hoặc recurring_schedules)
        - limit: Giới hạn số lượng kết quả
        
        Returns:
            List các tour_id thỏa mãn điều kiện
        """
        from datetime import date as date_type
        from repositories.tour_departure import TourDepartureRepository
        from repositories.tour_destination import TourDestinationRepository
        
        # Tìm tour_ids bằng embedding cho departure và destination
        tour_ids_by_departure = set()
        tour_ids_by_destination = set()
        
        if departure:
            dep_candidates = TourDepartureRepository.search_by_text(departure, limit=100)  # Lấy nhiều hơn để có đủ kết quả
            tour_ids_by_departure = {d.dict()["tour_id"] for d in dep_candidates}
        
        if destination:
            dest_candidates = TourDestinationRepository.search_by_text(destination, limit=100)  # Lấy nhiều hơn để có đủ kết quả
            tour_ids_by_destination = {d.dict()["tour_id"] for d in dest_candidates}
        
        # Kết hợp tour_ids từ departure và destination
        if departure and destination:
            # Phải thỏa mãn cả hai điều kiện
            candidate_tour_ids = tour_ids_by_departure.intersection(tour_ids_by_destination)
        elif departure:
            candidate_tour_ids = tour_ids_by_departure
        elif destination:
            candidate_tour_ids = tour_ids_by_destination
        else:
            candidate_tour_ids = None  # Không có điều kiện departure/destination
        
        with Session() as session:
            # Bắt đầu với query cơ bản từ bảng tours
            if candidate_tour_ids is not None:
                # Nếu có điều kiện departure/destination, filter theo tour_ids đã tìm được
                query = session.query(TourTable.id).filter(TourTable.id.in_(candidate_tour_ids)).distinct()
            else:
                query = session.query(TourTable.id).distinct()
            
            # Điều kiện 1: Lọc theo tour_type_id
            if tour_type_id is not None:
                query = query.filter(TourTable.tour_type_id == tour_type_id)
            
            # Điều kiện 2: Lọc theo ngày khởi hành 
            if target_date:
                if isinstance(target_date, str):
                    target_date = date_type.fromisoformat(target_date)
                
                # Subquery 1: Specific departures (Ngày khởi hành cụ thể)
                specific_subquery = (
                    session.query(DepartureSchedule.tour_id)
                    .join(SpecificDeparture, SpecificDeparture.schedule_id == DepartureSchedule.id)
                    .filter(
                        DepartureSchedule.tour_id == TourTable.id,
                        SpecificDeparture.date == target_date
                    )
                )
                
                # Subquery 2: Recurring schedules - Tìm theo NGÀY BẮT ĐẦU (start_date)
                recurring_subquery = (
                    session.query(DepartureSchedule.tour_id)
                    .join(RecurringSchedule, RecurringSchedule.schedule_id == DepartureSchedule.id)
                    .filter(
                        DepartureSchedule.tour_id == TourTable.id,
                        RecurringSchedule.start_date == target_date  # Chỉ tìm tour BẮT ĐẦU vào ngày này
                    )
                )
                
                # Kết hợp điều kiện: tour khởi hành vào ngày đó
                query = query.filter(
                    sa.or_(
                        specific_subquery.exists(),
                        recurring_subquery.exists()
                    )
                )
            
            # Giới hạn số lượng kết quả
            tour_ids = query.limit(limit).all()
            
            return [tid[0] for tid in tour_ids]


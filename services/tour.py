import uuid
from models.tour import TourCreateModel, TourUpdateModel, TourModel
from repositories.tour import TourRepository
from datetime import date
from repositories.tour_departure import TourDepartureRepository
from repositories.tour_destination import TourDestinationRepository
from repositories.tour_highlight_location import TourHighlightLocationRepository
from repositories.recurring_schedule import RecurringScheduleRepository
from repositories.specific_departure import SpecificDepartureRepository
from repositories.visa_price import VisaPriceRepository
from repositories.price_by_package import PriceByPackageRepository
from repositories.price_by_date import PriceByDateRepository

class TourService:
    @staticmethod
    def create(payload: TourCreateModel) -> TourModel:
        return TourRepository.create(payload)

    @staticmethod
    def get(tour_id: uuid.UUID):
        """
        Lấy thông tin chi tiết của 1 tour theo ID với format giống get_all_tours
        """
        
        # Lấy tour theo ID
        tour = TourRepository.get(tour_id)
        
        if not tour:
            return {"tours": []}

        tid = tour.id

        departures = [d.departure_name for d in TourDepartureRepository.get_by_tour_id(tid)]
        destinations = [d.destination_name for d in TourDestinationRepository.get_by_tour_id(tid)]
        hilghlights = [d.location_name for d in TourHighlightLocationRepository.get_by_tour_id(tid)]

        # schedules
        departure_schedules = []
        recurring_schedules = RecurringScheduleRepository.get_by_tour_id(tid)
        specific_departures = SpecificDepartureRepository.get_by_tour_id(tid)

        for r in recurring_schedules:
            departure_schedules.append({
                "schedule_type": "recurring",
                "recurrence_type": r.recurrence_type,
                "start_date": str(r.start_date),
                "end_date": str(r.end_date),
                "specific_dates": [],
                "weekdays": r.weekdays
            })

        if specific_departures:
            departure_schedules.append({
                "schedule_type": "specific",
                "specific_dates": [str(s.date) for s in specific_departures]
            })

        # prices
        visa_prices = [{"price": p.price} for p in VisaPriceRepository.get_by_tour_id(tid)]
        price_by_packages = [
            {"package_name": p.package_name, "price": p.price}
            for p in PriceByPackageRepository.get_by_tour_id(tid)
        ]
        price_by_dates = [
            {"date": str(p.date), "price": p.price}
            for p in PriceByDateRepository.get_by_tour_id(tid)
        ]

        tour_detail = {
            "tour_id": tour.id,
            "tour_name": tour.tour_name,
            "tour_type_id": tour.tour_type_id,
            "days": tour.days,
            "description": tour.description,
            "highlight": tour.highlight,
            "itinerary_url": tour.itinerary_url,
            "image_url": tour.image_url,
            "promotion_info": tour.promotion_info,
            "price_type": tour.price_type,
            "departures": departures,
            "destinations": destinations,
            "highlight_locations": hilghlights,
            "departure_schedules": departure_schedules,
            "visa_prices": visa_prices,
            "price_by_packages": price_by_packages,
            "price_by_dates": price_by_dates
        }

        return {"tours": [tour_detail]}

    @staticmethod
    def update(tour_id: uuid.UUID, payload: TourUpdateModel) -> TourModel | None:
        return TourRepository.update(tour_id, payload)

    @staticmethod
    def delete(tour_id: uuid.UUID) -> bool:
        return TourRepository.delete(tour_id)
    
    @staticmethod
    def delete_with_related(tour_id: uuid.UUID) -> bool:
        """
        Xóa tour và tất cả các bảng liên quan.
        """
        return TourRepository.delete_with_related(tour_id)

    @staticmethod
    def get_all() -> list[TourModel]:
        return TourRepository.get_all()

    @staticmethod
    def search_by_text(query: str, limit: int = 5):
        """
        Tìm kiếm tour theo text (semantic search).
        """
        return TourRepository.search_by_text(query=query, limit=limit)

    @staticmethod
    def tour_by_date(target_date: date):
        """
        Tìm kiếm tour theo ngày (dựa vào specific_departures / recurring_schedules / price_by_dates).
        """
        return TourRepository.tour_by_date(target_date)
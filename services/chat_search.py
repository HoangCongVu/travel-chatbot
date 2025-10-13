from datetime import date
from repositories.tour_departure import TourDepartureRepository
from repositories.tour_destination import TourDestinationRepository
from repositories.tour import TourRepository
from repositories.price_by_package import PriceByPackageRepository
from repositories.price_by_date import PriceByDateRepository
from repositories.visa_price import VisaPriceRepository
from repositories.departure_schedule import DepartureScheduleRepository
from repositories.recurring_schedule import RecurringScheduleRepository
from repositories.specific_departure import SpecificDepartureRepository

class ChatSearchService:
    @staticmethod
    def _get_full_tour_details(tour_id: int) -> dict | None:
        """
        Hàm private để lấy và định dạng TOÀN BỘ chi tiết của một tour.
        DRY - Don't Repeat Yourself.
        """
        tour = TourRepository.get(tour_id)
        if not tour:
            return None

        # Lấy thông tin liên quan
        departures = [d.departure_name for d in TourDepartureRepository.get_by_tour_id(tour_id)]
        destinations = [d.destination_name for d in TourDestinationRepository.get_by_tour_id(tour_id)]

        # Lấy lịch trình
        recurring_schedules = RecurringScheduleRepository.get_by_tour_id(tour_id)
        specific_departures = SpecificDepartureRepository.get_by_tour_id(tour_id)
        
        departure_schedules = []
        for r in recurring_schedules:
            departure_schedules.append({
                "schedule_type": "recurring",
                "recurrence_type": r.recurrence_type,
                "start_date": str(r.start_date),
                "end_date": str(r.end_date),
                "weekdays": r.weekdays
            })
        if specific_departures:
            departure_schedules.append({
                "schedule_type": "specific",
                "specific_dates": [str(s.date) for s in specific_departures]
            })
            
        # Lấy giá
        visa_prices = [{"price": p.price} for p in VisaPriceRepository.get_by_tour_id(tour_id)]
        price_by_packages = [
            {"package_name": p.package_name, "price": p.price}
            for p in PriceByPackageRepository.get_by_tour_id(tour_id)
        ]
        price_by_dates = [
            {"date": str(p.date), "price": p.price}
            for p in PriceByDateRepository.get_by_tour_id(tour_id)
        ]

        # Trả về một dictionary hoàn chỉnh
        return {
            "tour_name": tour.tour_name,
            "days": tour.days,
            "description": tour.description,
            "highlight": tour.highlight,
            "itinerary_url": tour.itinerary_url,
            "image_url": tour.image_url,
            "promotion_info": tour.promotion_info,
            "price_type": tour.price_type,
            "departures": departures,
            "destinations": destinations,
            "departure_schedules": departure_schedules,
            "visa_prices": visa_prices,
            "price_by_packages": price_by_packages,
            "price_by_dates": price_by_dates
        }

    @staticmethod
    def search_tour_by_destination(destination_text: str, limit: int = 5):
        dest_candidates = TourDestinationRepository.search_by_text(destination_text)
        dest_ids = {d.tour_id for d in dest_candidates}

        if not dest_ids:
            return {"tours": []}

        tours = []
        for tid in list(dest_ids)[:limit]:
            tour_details = ChatSearchService._get_full_tour_details(tid)
            if tour_details:
                tours.append(tour_details)
        
        return {"tours": tours}

    @staticmethod
    def search_tour_by_date(target_date: date, limit: int = 3):
        # Giả sử TourRepository.get_tour_ids_by_date trả về list các ID
        tour_ids = TourRepository.get_tour_ids_by_date(target_date) 
        if not tour_ids:
            return {"tours": []}

        tours = []
        for tid in tour_ids[:limit]:
            tour_details = ChatSearchService._get_full_tour_details(tid)
            if tour_details:
                tours.append(tour_details)
        
        return {"tours": tours}

    @staticmethod
    def search_tour_by_price(min_price: float = 0, max_price: float = 1e9, limit: int = 3):
        """
        Tìm tour theo khoảng giá - phiên bản hiệu quả hơn.
        GHI CHÚ: Cần cập nhật Repository để hỗ trợ các hàm này.
        """
        price_ids = set()

        # Giả định các hàm này chỉ query CSDL để lấy tour_id
        # Ví dụ: SELECT DISTINCT tour_id FROM price_by_package WHERE price BETWEEN ...
        package_tour_ids = PriceByPackageRepository.get_tour_ids_by_price_range(min_price, max_price)
        date_tour_ids = PriceByDateRepository.get_tour_ids_by_price_range(min_price, max_price)
        visa_tour_ids = VisaPriceRepository.get_tour_ids_by_price_range(min_price, max_price)

        price_ids.update(package_tour_ids)
        price_ids.update(date_tour_ids)
        price_ids.update(visa_tour_ids)
        
        if not price_ids:
            return {"tours": []}

        tours = []
        for tid in list(price_ids)[:limit]:
            tour_details = ChatSearchService._get_full_tour_details(tid)
            if tour_details:
                tours.append(tour_details)

        return {"tours": tours}
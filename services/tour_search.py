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
from repositories.tour_highlight_location import TourHighlightLocationRepository
from models.tour import SearchTour



class TourSearchService:
    @staticmethod
    def search_tour(departure_text: str, destination_text: str, limit: int = 5):
        dep_candidates = TourDepartureRepository.search_by_text(departure_text)
        dest_candidates = TourDestinationRepository.search_by_text(destination_text)

        dep_ids = {d.dict()["tour_id"] for d in dep_candidates}
        dest_ids = {d.dict()["tour_id"] for d in dest_candidates}

        common_ids = dep_ids.intersection(dest_ids)
        if not common_ids:
            return {"tours": []}

        tours = []
        for tid in list(common_ids)[:limit]:
            tour = TourRepository.get(tid)
            if not tour:
                continue

            departures = [d.departure_name for d in TourDepartureRepository.get_by_tour_id(tid)]
            destinations = [d.destination_name for d in TourDestinationRepository.get_by_tour_id(tid)]

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

            tours.append({
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
            })

        return {"tours": tours}


    @staticmethod
    def search_tour_by_destination(destination_text: str, limit: int = 5):
        dest_candidates = TourDestinationRepository.search_by_text(destination_text)
        dest_ids = {d.dict()["tour_id"] for d in dest_candidates}

        if not dest_ids:
            return {"tours": []}

        tours = []
        for tid in list(dest_ids)[:limit]:
            tour = TourRepository.get(tid)
            if not tour:
                continue

            departures = [d.departure_name for d in TourDepartureRepository.get_by_tour_id(tid)]
            destinations = [d.destination_name for d in TourDestinationRepository.get_by_tour_id(tid)]

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

            tours.append({
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
            })

        return {"tours": tours}


    @staticmethod
    def search_tour_by_date(target_date: date, limit: int = 5):
        tour_ids = TourRepository.tour_by_date(target_date)
        if not tour_ids:
            return {"tours": []}

        tours = []
        for tid in tour_ids[:limit]:
            tour = TourRepository.get(tid)
            if not tour:
                continue

            # departures & destinations (list string)
            departures = [d.departure_name for d in TourDepartureRepository.get_by_tour_id(tid)]
            destinations = [d.destination_name for d in TourDestinationRepository.get_by_tour_id(tid)]

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

            tours.append({
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
            })

        return {"tours": tours}

    @staticmethod
    def search_tour_by_price(min_price: float = 0, max_price: float = 1e9, limit: int = 5):
        """
        Tìm tour theo khoảng giá.
        min_price: giá tối thiểu
        max_price: giá tối đa
        """
        # Lấy tất cả tour có giá trong khoảng
        price_ids = set()

        # PriceByPackage
        package_tours = PriceByPackageRepository.get_all()
        for p in package_tours:
            if min_price <= p.price <= max_price:
                price_ids.add(p.tour_id)

        # PriceByDate
        date_tours = PriceByDateRepository.get_all()
        for p in date_tours:
            if min_price <= p.price <= max_price:
                price_ids.add(p.tour_id)

        # VisaPrice
        visa_tours = VisaPriceRepository.get_all()
        for v in visa_tours:
            if min_price <= v.price <= max_price:
                price_ids.add(v.tour_id)

        if not price_ids:
            return None

        # Gom thông tin tour, schedule, price
        results = []
        for tid in list(price_ids)[:limit]:
            tour = TourRepository.get(tid)
            if not tour:
                continue

            # Lấy schedule
            departure_schedules = DepartureScheduleRepository.get_by_tour_id(tid)
            recurring_schedules = RecurringScheduleRepository.get_by_tour_id(tid)
            specific_departures = SpecificDepartureRepository.get_by_tour_id(tid)

            # Lấy price
            package_prices = PriceByPackageRepository.get_by_tour_id(tid)
            date_prices = PriceByDateRepository.get_by_tour_id(tid)
            visa_prices = VisaPriceRepository.get_by_tour_id(tid)

            results.append({
                "tour": SearchTour.model_validate(tour),
                "schedules": {
                    "departure_schedules": departure_schedules,
                    "recurring_schedules": recurring_schedules,
                    "specific_departures": specific_departures
                },
                "prices": {
                    "by_package": package_prices,
                    "by_date": date_prices,
                    "visa": visa_prices
                }
            })

        return results[:limit]

    @staticmethod
    def get_all_tours():
        """
        Lấy tất cả tour với format giống search_tour
        """
        all_tours = TourRepository.get_all()
        
        if not all_tours:
            return {"tours": []}

        tours = []
        for tour in all_tours:  # Bỏ [:limit]
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

            tours.append({
                "tour_id": tour.id,
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
                "highlight_locations": hilghlights,
                "departure_schedules": departure_schedules,
                "visa_prices": visa_prices,
                "price_by_packages": price_by_packages,
                "price_by_dates": price_by_dates
            })

        return {"tours": tours}

    @staticmethod
    def search_tours_by_type(tour_type_id: int):
        """
        Tìm kiếm tour theo tour_type_id với format giống get_all_tours
        """
        # Lấy tours theo tour_type_id
        tours_by_type = TourRepository.search_by_tour_type(tour_type_id)
        
        if not tours_by_type:
            return {"tours": []}

        tours = []
        for tour in tours_by_type:
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

            tours.append({
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
            })

        return {"tours": tours}


    @staticmethod
    def search_tour_chat(destination: str = None, min_price: float = None, max_price: float = None, target_date = None, limit: int = 5):
        """
        Tìm kiếm tour với nhiều điều kiện kết hợp cho chatbot.
        
        Args:
            destination: Tên địa điểm đích (ví dụ: "Đà Lạt", "Singapore")
            min_price: Giá tối thiểu (VNĐ)
            max_price: Giá tối đa (VNĐ)
            target_date: Ngày khởi hành (date object hoặc string "YYYY-MM-DD")
            limit: Số lượng tour tối đa trả về (mặc định 5)
            
        Returns:
            Dict chứa danh sách tours với đầy đủ thông tin chi tiết
            
        Example:
            # Tìm tour đi Đà Lạt, giá từ 3-5 triệu, khởi hành ngày 15/7/2025
            result = TourSearchService.search_tour_chat(
                destination="Đà Lạt",
                min_price=3000000,
                max_price=5000000,
                target_date="2025-07-15",
                limit=3
            )
        """
        # Gọi repository để lấy danh sách tour_ids thỏa mãn điều kiện
        tour_ids = TourRepository.search_tour_chat(
            destination=destination,
            min_price=min_price,
            max_price=max_price,
            target_date=target_date,
            limit=limit
        )
        
        if not tour_ids:
            return {"tours": [], "message": "Không tìm thấy tour phù hợp với điều kiện tìm kiếm"}
        
        # Lấy thông tin chi tiết cho mỗi tour
        tours = []
        for tid in tour_ids:
            tour = TourRepository.get(tid)
            if not tour:
                continue

            # Lấy thông tin điểm khởi hành và đích đến
            departures = [d.departure_name for d in TourDepartureRepository.get_by_tour_id(tid)]
            destinations = [d.destination_name for d in TourDestinationRepository.get_by_tour_id(tid)]
            hilghlights = [h.location_name for h in TourHighlightLocationRepository.get_by_tour_id(tid)]

            # Lấy lịch trình khởi hành
            departure_schedules = []
            recurring_schedules = RecurringScheduleRepository.get_by_tour_id(tid)
            specific_departures = SpecificDepartureRepository.get_by_tour_id(tid)

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

            # Lấy thông tin giá
            visa_prices = [{"price": p.price} for p in VisaPriceRepository.get_by_tour_id(tid)]
            price_by_packages = [
                {"package_name": p.package_name, "price": p.price}
                for p in PriceByPackageRepository.get_by_tour_id(tid)
            ]
            price_by_dates = [
                {"date": str(p.date), "price": p.price}
                for p in PriceByDateRepository.get_by_tour_id(tid)
            ]

            tours.append({
                "tour_id": str(tour.id),
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
            })

        return {
            "tours": tours,
            "total_found": len(tours),
            "search_criteria": {
                "destination": destination,
                "min_price": min_price,
                "max_price": max_price,
                "target_date": str(target_date) if target_date else None
            }
        }

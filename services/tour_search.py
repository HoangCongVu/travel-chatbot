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

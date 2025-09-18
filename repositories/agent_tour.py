import json
import uuid
from agents.agent_tour import agent_tour_all
from services.tour import TourService
from services.tour_type import TourTypeService
from services.tour_destination import TourDestinationService
from services.tour_highlight_location import TourHighlightLocationService
from services.tour_departure import TourDepartureService
from services.visa_price import VisaPriceService
from services.price_by_package import PriceByPackageService
from services.price_by_date import PriceByDateService
from services.departure_schedule import DepartureScheduleService
from services.recurring_schedule import RecurringScheduleService
from services.specific_departure import SpecificDepartureService

from models.tour import TourCreateModel
from models.tour_type import CreateTourType, UpdateTourType
from models.tour_destination import CreateTourDestination
from models.tour_highlight_location import CreateTourHighlightLocation
from models.tour_departure import CreateTourDeparture
from models.visa_price import CreateVisaPrice
from models.price_by_package import CreatePriceByPackage
from models.price_by_date import CreatePriceByDate
from models.departure_schedule import CreateDepartureSchedule
from models.recurring_schedule import CreateRecurringSchedule
from models.specific_departure import CreateSpecificDeparture


class AgentTourRepository:

    @staticmethod
    def extract_from_text(payload: str):
        try:
            # -------------------------------
            # B1: Gọi agent duy nhất để lấy toàn bộ JSON
            # -------------------------------
            reply = agent_tour_all.generate_reply(
                messages=[{"role": "user", "content": payload}]
            )
            data = json.loads(reply)

            tours = data.get("tours", [])
            if not tours:
                raise ValueError("Không tìm thấy tour nào trong văn bản")

            # -------------------------------
            # B2: Lặp qua từng tour trong JSON
            # -------------------------------
            for tour in tours:
                # ---- TourType ----
                tour_type_id = tour["tour_type"]["tour_type_id"]
                tour_type_name = tour["tour_type"]["tour_type_name"]

                tour_type = TourTypeService.get(tour_type_id)
                if tour_type:
                    if tour_type.type_name != tour_type_name:
                        update_data = UpdateTourType(type_name=tour_type_name)
                        tour_type = TourTypeService.update(tour_type_id, update_data)
                else:
                    new_type = CreateTourType(id=tour_type_id, type_name=tour_type_name)
                    tour_type = TourTypeService.create(new_type)

                # ---- Tour Info ----
                tour_data = {
                    "tour_name": tour["tour_name"],
                    "days": tour["days"],
                    "description": tour.get("description", ""),
                    "highlight": tour.get("highlight", ""),
                    "itinerary_url": tour.get("itinerary_url", ""),
                    "detail_url": tour.get("detail_url", ""),
                    "promotion_info": tour.get("promotion_info", ""),
                    "price_type": tour.get("price_type", "Một giá"),
                    "tour_type_id": tour_type.id,
                }
                new_tour = TourCreateModel(**tour_data)
                new_tour = TourService.create(new_tour)

                # ---- Departures ----
                for dep in tour.get("departures", []):
                    record = CreateTourDeparture(tour_id=new_tour.id, departure_name=dep)
                    TourDepartureService.create(record)

                # ---- Destinations ----
                for dest in tour.get("destinations", []):
                    record = CreateTourDestination(tour_id=new_tour.id, destination_name=dest)
                    TourDestinationService.create(record)

                # ---- Highlight Locations ----
                for loc in tour.get("highlight_locations", []):
                    record = CreateTourHighlightLocation(tour_id=new_tour.id, location_name=loc)
                    TourHighlightLocationService.create(record)

                # ---- Departure Schedules ----
                for sched in tour.get("departure_schedules", []):
                    dep_schedule_record = CreateDepartureSchedule(
                        tour_id=new_tour.id, schedule_type=sched.get("schedule_type")
                    )
                    dep_schedule = DepartureScheduleService.create(dep_schedule_record)

                    if sched["schedule_type"] == "recurring":
                        recurring_record = CreateRecurringSchedule(
                            schedule_id=dep_schedule.id,
                            recurrence_type=sched.get("recurrence_type", "custom"),
                            start_date=sched["start_date"],
                            end_date=sched["end_date"],
                            weekdays=sched.get("weekdays", []),
                        )
                        RecurringScheduleService.create(recurring_record)

                    elif sched["schedule_type"] == "specific":
                        for date in sched.get("specific_dates", []):
                            specific_record = CreateSpecificDeparture(
                                schedule_id=dep_schedule.id, date=date
                            )
                            SpecificDepartureService.create(specific_record)

                # ---- Prices ----
                for item in tour.get("visa_prices", []):
                    record = CreateVisaPrice(tour_id=new_tour.id, price=item.get("price"))
                    VisaPriceService.create(record)

                for item in tour.get("price_by_packages", []):
                    record = CreatePriceByPackage(
                        tour_id=new_tour.id,
                        package_name=item.get("package_name"),
                        price=item.get("price"),
                    )
                    PriceByPackageService.create(record)

                for item in tour.get("price_by_dates", []):
                    record = CreatePriceByDate(
                        tour_id=new_tour.id, date=item.get("date"), price=item.get("price")
                    )
                    PriceByDateService.create(record)

            return {"Tours": tours}

        except Exception as e:
            print("❌ Lỗi khi xử lý tour:", str(e))
            return {
                "error": "Không thể xử lý dữ liệu đầu vào",
                "message": str(e),
            }

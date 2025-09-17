import uuid
import json
from agents.agent_tour_location import agent_tour_location
from services.tour_destination import TourDestinationService
from services.tour_highlight_location import TourHighlightLocationService
from services.tour_departure import TourDepartureService
from models.tour_destination import CreateTourDestination
from models.tour_highlight_location import CreateTourHighlightLocation
from models.tour_departure import CreateTourDeparture
from env import env

class AgentTourLocationRepository:
    def extract_info_from_text(payload: str, tour_id: uuid.UUID) -> dict:
        try:
            # B1: Gọi agent để lấy JSON
            reply = agent_tour_location.generate_reply(
                messages=[{"role": "user", "content": payload}]
            )

            data = json.loads(reply)

            departures = data.get("departures", [])
            highlights = data.get("highlight_locations", [])
            destinations = data.get("destinations", [])

            # B2: Insert vào DB
            for dep in departures:
                record = CreateTourDeparture(
                    tour_id=tour_id,
                    departure_name=dep
                )
                TourDepartureService.create(record)

            for loc in highlights:
                record = CreateTourHighlightLocation(
                    tour_id=tour_id,
                    location_name=loc
                )
                TourHighlightLocationService.create(record)

            for dest in destinations:
                record = CreateTourDestination(
                    tour_id=tour_id,
                    destination_name=dest
                )
                TourDestinationService.create(record)            

            # B3: Return kết quả
            return {
                "tour_id": tour_id,
                "departures": departures,
                "destinations": destinations,
                "highlight_locations": highlights
            }

        except Exception as e:
            print("Lỗi khi trích xuất tour meta:", str(e))
            return {
                "error": "Không thể xử lý dữ liệu đầu vào",
                "message": str(e)
            }

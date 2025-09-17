import uuid
from repositories.agent_tour_location import AgentTourLocationRepository

class AgentTourLocationService:
    @staticmethod
    def extract_info_from_text(payload: str, tour_id: uuid.UUID):
        return AgentTourLocationRepository.extract_info_from_text(payload, tour_id)

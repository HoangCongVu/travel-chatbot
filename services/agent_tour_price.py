import uuid
from repositories.agent_tour_price import AgentTourPriceRepository

class AgentTourPriceService:
    @staticmethod
    def extract_info_from_text(payload: str, tour_id: uuid.UUID):
        return AgentTourPriceRepository.extract_prices_from_text(payload, tour_id)

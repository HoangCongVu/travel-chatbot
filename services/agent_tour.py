import uuid
from repositories.agent_tour import AgentTourRepository


class AgentTourService:
    @staticmethod
    def extract_info_from_text(payload: str):
        """
        Extract toàn bộ thông tin tour từ payload bằng AgentTourRepository.
        """
        return AgentTourRepository.extract_from_text(payload)

from repositories.agent_tour_info import AgentTourInfoRepository

class AgentTourInfoService:
    @staticmethod
    def extract_info_from_text(payload: str):
        return AgentTourInfoRepository.extract_info_from_text(payload)
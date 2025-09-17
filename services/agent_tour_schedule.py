import uuid
from repositories.agent_tour_schedule import AgentTourScheduleRepository

class AgentTourScheduleService:
    @staticmethod
    def extract_info_from_text(payload: str, tour_id: uuid.UUID):
        return AgentTourScheduleRepository.extract_schedules_from_text(payload, tour_id)

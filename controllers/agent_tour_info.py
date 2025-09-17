from fastapi import APIRouter
from pydantic import BaseModel
from services.agent_tour_info import AgentTourInfoService
import uuid
router = APIRouter(prefix="/tour", tags=["tour"])

# Schema input
class TourText(BaseModel):
    text: str

@router.post("/tour-info")
async def extract_tour_info(payload: TourText):
    result = AgentTourInfoService.extract_info_from_text(payload.text)
    return result
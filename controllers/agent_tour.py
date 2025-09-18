from fastapi import APIRouter
from pydantic import BaseModel
from services.agent_tour import AgentTourService
import uuid

router = APIRouter(prefix="/tour", tags=["tour"])

# Schema input
class TourText(BaseModel):
    text: str

@router.post("/agent-tour")
async def extract_tour(payload: TourText):
    result = AgentTourService.extract_info_from_text(payload.text)
    return result
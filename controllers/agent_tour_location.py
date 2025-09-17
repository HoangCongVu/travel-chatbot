from fastapi import APIRouter
from pydantic import BaseModel
from services.agent_tour_location import AgentTourLocationService
import uuid
router = APIRouter(prefix="/tour", tags=["tour"])

# Schema input
class TourText(BaseModel):
    text: str

@router.post("/tour-location")
async def extract_tour_location(payload: TourText):
    fake_tour_id = uuid.UUID("9b97a60a-3f9f-4dbf-82dd-a071f53923d8")
    result = AgentTourLocationService.extract_info_from_text(payload.text, fake_tour_id)
    return result
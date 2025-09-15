import uuid
from fastapi import APIRouter
from models.tour_highlight_location import (
    CreateTourHighlightLocationPayload,
    UpdateTourHighlightLocationPayload,
    TourHighlightLocationModel
)
from services.tour_highlight_location import TourHighlightLocationService

router = APIRouter(prefix="/tour-highlight-locations", tags=["Tour Highlight Locations"])


@router.post("", response_model=TourHighlightLocationModel)
def create_location(payload: CreateTourHighlightLocationPayload):
    return TourHighlightLocationService.create(payload)


@router.get("", response_model=TourHighlightLocationModel)
def get_location(location_id: uuid.UUID):
    return TourHighlightLocationService.get(location_id)


@router.put("", response_model=TourHighlightLocationModel)
def update_location(location_id: uuid.UUID, payload: UpdateTourHighlightLocationPayload):
    return TourHighlightLocationService.update(location_id, payload)


@router.delete("")
def delete_location(location_id: uuid.UUID):
    TourHighlightLocationService.delete(location_id)
    return {"message": "Tour highlight location deleted successfully"}
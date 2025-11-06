import uuid
from fastapi import APIRouter
from models.tour_highlight_location import CreateTourHighlightLocation, UpdateTourHighlightLocation, TourHighlightLocationModel
from services.tour_highlight_location import TourHighlightLocationService


router = APIRouter(prefix="/tour-highlight-locations", tags=["Tour Highlight Locations"])


@router.post("/create", response_model=TourHighlightLocationModel)
def create_location(payload: CreateTourHighlightLocation):
    return TourHighlightLocationService.create(payload)

@router.put("/update-by-tour", response_model=list[TourHighlightLocationModel])
def update_location_by_tour(tour_id: uuid.UUID, payload: UpdateTourHighlightLocation):
    return TourHighlightLocationService.update_by_tour_id(tour_id, payload)

@router.delete("")
def delete_location(location_id: uuid.UUID):
    TourHighlightLocationService.delete(location_id)
    return {"message": "Tour highlight location deleted successfully"}
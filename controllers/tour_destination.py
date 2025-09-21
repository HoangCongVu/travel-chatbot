import uuid
from fastapi import APIRouter, Query
from models.tour_destination import CreateTourDestination, UpdateTourDestination, TourDestinationModel

from services.tour_destination import TourDestinationService
router = APIRouter(prefix="/tour-destinations", tags=["Tour Destinations"])


@router.post("", response_model=TourDestinationModel)
def create_destination(payload: CreateTourDestination):
    return TourDestinationService.create(payload)


@router.get("", response_model=TourDestinationModel)
def get_destination(destination_id: uuid.UUID):
    return TourDestinationService.get(destination_id)


@router.put("", response_model=TourDestinationModel)
def update_destination(destination_id: uuid.UUID, payload: UpdateTourDestination):
    return TourDestinationService.update(destination_id, payload)


@router.delete("")
def delete_destination(destination_id: uuid.UUID):
    TourDestinationService.delete(destination_id)
    return {"message": "Tour destination deleted successfully"}

@router.get("/search-text")
def search_tour_destinations(
    query: str = Query(..., description="Từ khóa tìm kiếm tour destination"),
    limit: int = Query(5, description="Số lượng kết quả tối đa")
):
    """
    API tìm kiếm tour destination theo text (semantic search).
    """
    return TourDestinationService.search_by_text(query=query, limit=limit)
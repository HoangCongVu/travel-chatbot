import uuid
from fastapi import APIRouter, Query
from models.tour_destination import CreateTourDestination, UpdateTourDestination, TourDestinationModel

from services.tour_destination import TourDestinationService
router = APIRouter(prefix="/tour-destinations", tags=["Tour Destinations"])


@router.post("/create", response_model=TourDestinationModel)
def create_destination(payload: CreateTourDestination):
    return TourDestinationService.create(payload)

@router.put("/update-by-tour", response_model=list[TourDestinationModel])
def update_destination_by_tour(tour_id: uuid.UUID, payload: UpdateTourDestination):
    return TourDestinationService.update_by_tour_id(tour_id, payload)

# @router.delete("")
# def delete_destination(destination_id: uuid.UUID):
#     TourDestinationService.delete(destination_id)
#     return {"message": "Tour destination deleted successfully"}

@router.get("/search-text")
def search_tour_destinations(
    query: str = Query(..., description="Từ khóa tìm kiếm tour destination"),
    limit: int = Query(5, description="Số lượng kết quả tối đa")
):
    """
    API tìm kiếm tour destination theo text (semantic search).
    """
    return TourDestinationService.search_by_text(query=query, limit=limit)
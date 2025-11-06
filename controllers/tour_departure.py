import uuid
from fastapi import APIRouter, Query
from models.tour_departure import CreateTourDeparture, UpdateTourDeparture, TourDepartureModel
from services.tour_departure import TourDepartureService


router = APIRouter(prefix="/tour-departures", tags=["Tour Departures"])


@router.post("/create", response_model=TourDepartureModel)
def create_departure(payload: CreateTourDeparture):
    return TourDepartureService.create(payload)


# @router.get("", response_model=TourDepartureModel)
# def get_departure(departure_id: uuid.UUID):
#     return TourDepartureService.get(departure_id)


# @router.put("/update", response_model=TourDepartureModel)
# def update_departure(departure_id: uuid.UUID, payload: UpdateTourDeparture):
#     return TourDepartureService.update(departure_id, payload)

@router.put("/update-by-tour", response_model=list[TourDepartureModel])
def update_departure_by_tour(tour_id: uuid.UUID, payload: UpdateTourDeparture):
    return TourDepartureService.update_by_tour_id(tour_id, payload)

# @router.delete("")
# def delete_departure(departure_id: uuid.UUID):
#     TourDepartureService.delete(departure_id)
#     return {"message": "Tour departure deleted successfully"}

@router.get("/search-text")
def search_tour_departures(
    query: str = Query(..., description="Từ khóa tìm kiếm tour departure"),
    limit: int = Query(5, description="Số lượng kết quả tối đa")
):
    """
    API tìm kiếm tour departure theo text (semantic search).
    """
    return TourDepartureService.search_by_text(query=query, limit=limit)

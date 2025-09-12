import uuid
from fastapi import APIRouter
from models.tour import TourCreateModel, TourModel
from services.tour import TourService

router = APIRouter(prefix="/tours", tags=["Tours"])

@router.post("", response_model=TourModel)
def create_tour(tour: TourCreateModel):
    return TourService.create_tour(tour)

@router.get("", response_model=TourModel)
def get_tour(tour_id:uuid.UUID):
    return TourService.get_tour(tour_id)

@router.put("", response_model=TourModel)
def update_tour(tour_id: uuid.UUID, tour: TourCreateModel):
    return TourService.update(tour_id, tour)

@router.delete("")
def delete_tour(tour_id: uuid.UUID):
    return TourService.delete_tour(tour_id)

@router.get("/", response_model=list[TourModel])
def get_all_tour():
    return TourService.get_all_tour()

@router.get("")
async def get_tour_info(tour_id: uuid.UUID):
    return TourService.get_tour_info(tour_id)
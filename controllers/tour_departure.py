import uuid
from fastapi import APIRouter
from models.tour_departure import (
    CreateTourDeparturePayload,
    UpdateTourDeparturePayload,
    TourDepartureModel
)
from services.tour_departure import TourDepartureService


router = APIRouter(prefix="/tour-departures", tags=["Tour Departures"])


@router.post("", response_model=TourDepartureModel)
def create_departure(payload: CreateTourDeparturePayload):
    return TourDepartureService.create(payload)


@router.get("", response_model=TourDepartureModel)
def get_departure(departure_id: uuid.UUID):
    return TourDepartureService.get(departure_id)


@router.put("", response_model=TourDepartureModel)
def update_departure(departure_id: uuid.UUID, payload: UpdateTourDeparturePayload):
    return TourDepartureService.update(departure_id, payload)


@router.delete("")
def delete_departure(departure_id: uuid.UUID):
    TourDepartureService.delete(departure_id)
    return {"message": "Tour departure deleted successfully"}
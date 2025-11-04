import uuid
from fastapi import APIRouter
from models.specific_departure import CreateSpecificDeparture, UpdateSpecificDeparture, SpecificDepartureModel
from services.specific_departure import SpecificDepartureService


router = APIRouter(prefix="/specific-departures", tags=["Specific Departures"])


@router.post("/create", response_model=SpecificDepartureModel)
def create_departure(payload: CreateSpecificDeparture):
    return SpecificDepartureService.create(payload)


@router.get("", response_model=SpecificDepartureModel)
def get_departure(specific_departure_id: uuid.UUID):
    return SpecificDepartureService.get(specific_departure_id)


@router.put("/update", response_model=SpecificDepartureModel)
def update_departure(specific_departure_id: uuid.UUID, payload: UpdateSpecificDeparture):
    return SpecificDepartureService.update(specific_departure_id, payload)


@router.delete("")
def delete_departure(specific_departure_id: uuid.UUID):
    SpecificDepartureService.delete(specific_departure_id)
    return {"message": "Specific departure deleted successfully"}
import uuid
from fastapi import APIRouter
from models.specific_departure import (
    CreateSpecificDeparturePayload,
    UpdateSpecificDeparturePayload,
    SpecificDepartureModel
)
from services.specific_departure import SpecificDepartureService

router = APIRouter(prefix="/specific-departures", tags=["Specific Departures"])


@router.post("", response_model=SpecificDepartureModel)
def create_departure(payload: CreateSpecificDeparturePayload):
    return SpecificDepartureService.create(payload)


@router.get("", response_model=SpecificDepartureModel)
def get_departure(departure_id: uuid.UUID):
    return SpecificDepartureService.get(departure_id)


@router.put("", response_model=SpecificDepartureModel)
def update_departure(departure_id: uuid.UUID, payload: UpdateSpecificDeparturePayload):
    return SpecificDepartureService.update(departure_id, payload)


@router.delete("")
def delete_departure(departure_id: uuid.UUID):
    SpecificDepartureService.delete(departure_id)
    return {"message": "Specific departure deleted successfully"}
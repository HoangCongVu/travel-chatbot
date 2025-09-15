import uuid
from fastapi import APIRouter
from models.tour_destination import (
    CreateTourDestinationPayload,
    UpdateTourDestinationPayload,
    TourDestinationModel
)
from services.tour_destination import TourDestinationService
router = APIRouter(prefix="/tour-destinations", tags=["Tour Destinations"])


@router.post("", response_model=TourDestinationModel)
def create_destination(payload: CreateTourDestinationPayload):
    return TourDestinationService.create(payload)


@router.get("", response_model=TourDestinationModel)
def get_destination(destination_id: uuid.UUID):
    return TourDestinationService.get(destination_id)


@router.put("", response_model=TourDestinationModel)
def update_destination(destination_id: uuid.UUID, payload: UpdateTourDestinationPayload):
    return TourDestinationService.update(destination_id, payload)


@router.delete("")
def delete_destination(destination_id: uuid.UUID):
    TourDestinationService.delete(destination_id)
    return {"message": "Tour destination deleted successfully"}
from fastapi import APIRouter
from models.tour_type import (
    CreateTourType,
    UpdateTourType,
    TourTypeModel
)
from services.tour_type import TourTypeService

router = APIRouter(prefix="/tour-types", tags=["Tour Types"])


@router.post("", response_model=TourTypeModel)
def create_type(payload: CreateTourType):
    return TourTypeService.create(payload)


@router.get("", response_model=TourTypeModel)
def get_type(type_id: int):
    return TourTypeService.get(type_id)

@router.get("/by-name", response_model=TourTypeModel | None)
def get_type_by_name(type_name: str):
    return TourTypeService.get_by_name(type_name)

@router.put("", response_model=TourTypeModel)
def update_type(type_id: int, payload: UpdateTourType):
    return TourTypeService.update(type_id, payload)


@router.delete("")
def delete_type(type_id: int):
    TourTypeService.delete(type_id)
    return {"message": "Tour type deleted successfully"}
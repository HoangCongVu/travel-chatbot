from fastapi import APIRouter
import uuid
from models.price_by_package import (
    CreatePriceByPackagePayload,
    UpdatePriceByPackagePayload,
    PriceByPackageModel
)
from services.price_by_package import PriceByPackageService

router = APIRouter(prefix="/price-by-packages", tags=["Price By Packages"])


@router.post("", response_model=PriceByPackageModel)
def create_price(payload: CreatePriceByPackagePayload):
    return PriceByPackageService.create(payload)


@router.get("", response_model=PriceByPackageModel)
def get_price(record_id: uuid.UUID):
    return PriceByPackageService.get(record_id)


@router.put("", response_model=PriceByPackageModel)
def update_price(record_id: uuid.UUID, payload: UpdatePriceByPackagePayload):
    return PriceByPackageService.update(record_id, payload)


@router.delete("")
def delete_price(record_id: uuid.UUID):
    PriceByPackageService.delete(record_id)
    return {"message": "Price by package deleted successfully"}
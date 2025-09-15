import uuid
from fastapi import APIRouter
from models.price_by_date import (
    CreatePriceByDatePayload,
    UpdatePriceByDatePayload,
    PriceByDateModel
)
from services.price_by_date import PriceByDateService

router = APIRouter(prefix="/price-by-dates", tags=["Price By Dates"])


@router.post("", response_model=PriceByDateModel)
def create_price(payload: CreatePriceByDatePayload):
    return PriceByDateService.create(payload)


@router.get("", response_model=PriceByDateModel)
def get_price(price_id: uuid.UUID):
    return PriceByDateService.get(price_id)


@router.put("", response_model=PriceByDateModel)
def update_price(price_id: uuid.UUID, payload: UpdatePriceByDatePayload):
    return PriceByDateService.update(price_id, payload)


@router.delete("")
def delete_price(price_id: uuid.UUID):
    PriceByDateService.delete(price_id)
    return {"message": "Price by date deleted successfully"}
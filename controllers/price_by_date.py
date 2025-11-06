import uuid
from fastapi import APIRouter
from models.price_by_date import CreatePriceByDate, UpdatePriceByDate, PriceByDateModel
from services.price_by_date import PriceByDateService

router = APIRouter(prefix="/price-by-dates", tags=["Price By Dates"])


@router.post("/create", response_model=PriceByDateModel)
def create_price(payload: CreatePriceByDate):
    return PriceByDateService.create(payload)

@router.put("/update-by-tour", response_model=list[PriceByDateModel])
def update_price_by_tour(tour_id: uuid.UUID, payload: UpdatePriceByDate):
    return PriceByDateService.update_by_tour_id(tour_id, payload)

@router.delete("")
def delete_price(price_id: uuid.UUID):
    PriceByDateService.delete(price_id)
    return {"message": "Price by date deleted successfully"}
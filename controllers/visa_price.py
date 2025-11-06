import uuid
from fastapi import APIRouter
from models.visa_price import CreateVisaPrice, VisaPriceModel, UpdateVisaPrice
from services.visa_price import VisaPriceService

router = APIRouter(prefix="/visa-price", tags=["Visa Price"])

@router.post("/create", response_model=VisaPriceModel)
def create_visa_price(payload: CreateVisaPrice):
    return VisaPriceService.create(payload)

@router.put("/by-tour", response_model=list[VisaPriceModel])
def update_visa_price_by_tour(tour_id: uuid.UUID, visa_price: UpdateVisaPrice):
    return VisaPriceService.update_by_tour_id(tour_id, visa_price)

@router.delete("")
def delete_visa_price(visa_price_id: uuid.UUID):
    return VisaPriceService.delete_visa_price(visa_price_id)

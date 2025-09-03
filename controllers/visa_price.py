import uuid
from fastapi import APIRouter
from models.visa_price import CreateVisaPrice, VisaPriceModel
from services.visa_price import VisaPriceService

router = APIRouter(prefix="/visa-pice", tags=["Visa Price"])

@router.post("", response_model=VisaPriceModel)
def create_visa_price(payload: CreateVisaPrice):
    return VisaPriceService.create_visa_price(payload)

@router.get("", response_model=VisaPriceModel)
def get_visa_price(visa_price_id: uuid.UUID):
    return VisaPriceService.get_visa_price(visa_price_id)

@router.put("", response_model=VisaPriceModel)
def update_visa_price(visa_price_id: uuid.UUID, visa_price: CreateVisaPrice):
    return VisaPriceService.update_visa_price(visa_price_id, visa_price)
@router.delete("")
def delete_visa_price(visa_price_id: uuid.UUID):
    return VisaPriceService.delete_visa_price(visa_price_id)
@router.get("", response_model=list[VisaPriceModel])
def get_all_visa_price():
    return VisaPriceService.get_all_visa_price()
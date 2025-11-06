from fastapi import APIRouter
import uuid
from models.price_by_package import CreatePriceByPackage, UpdatePriceByPackage, PriceByPackageModel
from services.price_by_package import PriceByPackageService


router = APIRouter(prefix="/price-by-packages", tags=["Price By Packages"])


@router.post("/create", response_model=PriceByPackageModel)
def create_price(payload: CreatePriceByPackage):
    return PriceByPackageService.create(payload)

@router.put("/update-by-tour", response_model=list[PriceByPackageModel])
def update_price_by_tour(tour_id: uuid.UUID, payload: UpdatePriceByPackage):
    return PriceByPackageService.update_by_tour_id(tour_id, payload)


@router.delete("")
def delete_price(record_id: uuid.UUID):
    PriceByPackageService.delete(record_id)
    return {"message": "Price by package deleted successfully"}
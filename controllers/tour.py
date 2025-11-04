import uuid
from fastapi import APIRouter, Query, Depends
from models.tour import TourCreateModel, TourUpdateModel, TourModel
from services.tour import TourService
from services.tour_search import TourSearchService
from middleware.auth import get_current_admin

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/search-text")
def search_tour(
    query: str = Query(..., description="Từ khóa tìm kiếm tour"),
    limit: int = Query(5, description="Số lượng kết quả tối đa")
):
    """
    API tìm kiếm tour theo text (semantic search).
    """
    return TourService.search_by_text(query=query, limit=limit)

@router.post("/create", response_model=TourModel)
def create_tour(
    tour: TourCreateModel,
    current_admin: str = Depends(get_current_admin)
):
    """Tạo tour mới - Chỉ admin được phép"""
    return TourService.create(tour)


@router.get("/{tour_id}", response_model=TourModel | None)
def get_tour(tour_id: uuid.UUID):
    """Lấy thông tin 1 tour theo ID"""
    return TourService.get(tour_id)


@router.put("/update/{tour_id}", response_model=TourModel | None)
def update_tour(
    tour_id: uuid.UUID, 
    tour: TourUpdateModel,
    current_admin: str = Depends(get_current_admin)
):
    """Cập nhật thông tin tour theo ID - Chỉ admin được phép"""
    return TourService.update(tour_id, tour)


@router.delete("/{tour_id}")
def delete_tour(
    tour_id: uuid.UUID,
    current_admin: str = Depends(get_current_admin)
):
    """Xóa tour theo ID - Chỉ admin được phép"""
    TourService.delete(tour_id)
    return {"message": "Tour deleted successfully"}


@router.delete("/delete/{tour_id}")
def delete_tour_with_related(
    tour_id: uuid.UUID,
    current_admin: str = Depends(get_current_admin)
):
    """
    Xóa tour và tất cả các bảng liên quan - Chỉ admin được phép
    Bao gồm:
    - departure_schedules (và cascade: specific_departures, recurring_schedules)
    - visa_prices
    - tour_highlight_locations
    - tour_destinations
    - tour_departures
    - price_by_packages
    - price_by_dates
    """
    result = TourService.delete_with_related(tour_id)
    if result:
        return {"message": "Tour and all related data deleted successfully"}
    else:
        return {"message": "Tour not found", "status": 404}


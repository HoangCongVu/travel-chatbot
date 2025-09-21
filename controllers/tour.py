import uuid
from fastapi import APIRouter, Query
from models.tour import TourCreateModel, TourUpdateModel, TourModel
from services.tour import TourService

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

@router.post("", response_model=TourModel)
def create_tour(tour: TourCreateModel):
    """Tạo tour mới"""
    return TourService.create(tour)


@router.get("/{tour_id}", response_model=TourModel | None)
def get_tour(tour_id: uuid.UUID):
    """Lấy thông tin 1 tour theo ID"""
    return TourService.get(tour_id)


@router.put("/{tour_id}", response_model=TourModel | None)
def update_tour(tour_id: uuid.UUID, tour: TourUpdateModel):
    """Cập nhật thông tin tour theo ID"""
    return TourService.update(tour_id, tour)


@router.delete("/{tour_id}")
def delete_tour(tour_id: uuid.UUID):
    """Xóa tour theo ID"""
    TourService.delete(tour_id)
    return {"message": "Tour deleted successfully"}


@router.get("/", response_model=list[TourModel])
def get_all_tour():
    """Lấy danh sách tất cả các tour"""
    return TourService.get_all()
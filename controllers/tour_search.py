from fastapi import APIRouter, Query, HTTPException
from services.tour_search import TourSearchService
from datetime import date

router = APIRouter(prefix="/search-tours", tags=["Tourssearch"])

@router.get("/")
def search_tours(
    departure: str = Query(..., description="Điểm xuất phát (VD: Hà Nội)"),
    destination: str = Query(..., description="Điểm đến (VD: Đà Nẵng)")
):
    results = TourSearchService.search_tour(departure, destination)
    
    if not results or len(results) == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy tour phù hợp")

    return {
        "status": "success",
        "total_results": len(results),
        "data": results
    }

@router.get("/by-destination/")
def search_tours_by_destination(
    destination: str = Query(..., description="Điểm đến (VD: Đà Nẵng)")
):
    results = TourSearchService.search_tour_by_destination(destination)

    if not results or len(results) == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy tour phù hợp")

    return {
        "status": "success",
        "total_results": len(results),
        "data": results
    }
    
@router.get("/by-date/")
def search_tours_by_date(
    target_date: date = Query(..., description="Ngày khởi hành (VD: 2025-12-20)")
):
    results = TourSearchService.search_tour_by_date(target_date)

    if not results or len(results) == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy tour phù hợp trong ngày này")

    return {
        "status": "success",
        "total_results": len(results),
        "data": results
    }

@router.get("/by-price/")
def search_tours_by_price(
    min_price: float = Query(0, description="Giá tối thiểu"),
    max_price: float = Query(1e9, description="Giá tối đa")
):
    results = TourSearchService.search_tour_by_price(min_price=min_price, max_price=max_price)

    if not results or len(results) == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy tour phù hợp trong khoảng giá này")

    return {
        "status": "success",
        "total_results": len(results),
        "data": results
    }

@router.get("/all/")
def get_all_tours():
    """
    Lấy tất cả tour có sẵn
    """
    results = TourSearchService.get_all_tours()

    if not results or not results.get("tours"):
        raise HTTPException(status_code=404, detail="Không có tour nào")

    return {
        "status": "success",
        "total_results": len(results["tours"]),
        "data": results
    }

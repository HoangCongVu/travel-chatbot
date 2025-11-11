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

@router.get("/tourpage/")
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

@router.get("/search-by-type/{tour_type_id}")
def search_tour_by_type(tour_type_id: int):
    """
    API tìm kiếm tour theo tour_type_id.
    """
    return TourSearchService.search_tours_by_type(tour_type_id)


@router.get("/chat-search/")
def search_tour_chat(
    destination: str = Query(None, description="Điểm đến (VD: Đà Lạt, Singapore)"),
    min_price: float = Query(None, description="Giá tối thiểu (VNĐ)"),
    max_price: float = Query(None, description="Giá tối đa (VNĐ)"),
    target_date: date = Query(None, description="Ngày khởi hành (VD: 2025-07-15)"),
    limit: int = Query(5, description="Số lượng tour tối đa", ge=1, le=20)
):
    """
    API tìm kiếm tour với nhiều điều kiện kết hợp (dành cho chatbot).
    
    Có thể tìm kiếm theo:
    - destination: Tên địa điểm đích
    - min_price, max_price: Khoảng giá
    - target_date: Ngày khởi hành
    - Hoặc kết hợp nhiều điều kiện
    
    Ví dụ:
    - /chat-search/?destination=Đà Lạt
    - /chat-search/?min_price=3000000&max_price=5000000
    - /chat-search/?destination=Đà Lạt&target_date=2025-07-15
    - /chat-search/?destination=Đà Lạt&min_price=2000000&max_price=8000000&target_date=2025-07-15
    """
    # Kiểm tra ít nhất một điều kiện được cung cấp
    if not any([destination, min_price, max_price, target_date]):
        raise HTTPException(
            status_code=400, 
            detail="Vui lòng cung cấp ít nhất một điều kiện tìm kiếm (destination, min_price, max_price, hoặc target_date)"
        )
    
    results = TourSearchService.search_tour_chat(
        destination=destination,
        min_price=min_price,
        max_price=max_price,
        target_date=target_date,
        limit=limit
    )

    if not results.get("tours"):
        return {
            "status": "not_found",
            "message": results.get("message", "Không tìm thấy tour phù hợp"),
            "search_criteria": results.get("search_criteria"),
            "data": {"tours": []}
        }

    return {
        "status": "success",
        "total_found": results["total_found"],
        "search_criteria": results["search_criteria"],
        "data": results
    }
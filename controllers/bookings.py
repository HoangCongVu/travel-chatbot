import uuid
from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel, Field
from models.bookings import BookingModel, BookingCreateModel, BookingUpdateModel, BookingWithCartItemModel
from services.bookings import BookingService
from middleware.auth import get_current_admin, get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class CheckoutUserRequest(BaseModel):
    """Request body cho checkout - User đã đăng nhập"""
    cart_id: uuid.UUID
    adult_count: int = Field(ge=1, description="Số người lớn")
    child_count: int = Field(default=0, ge=0, description="Số trẻ em")
    special_request: str | None = None
    meta_data: dict | None = None


class CheckoutGuestRequest(BaseModel):
    """Request body cho checkout - Khách vãng lai"""
    cart_id: uuid.UUID
    session_id: uuid.UUID = Field(description="Session ID của guest")
    guest_name: str = Field(min_length=1, description="Tên khách hàng")
    guest_phone: str = Field(min_length=1, description="Số điện thoại")
    guest_email: str = Field(min_length=1, description="Email")
    adult_count: int = Field(ge=1, description="Số người lớn")
    child_count: int = Field(default=0, ge=0, description="Số trẻ em")
    special_request: str | None = None
    meta_data: dict | None = None


@router.post("/checkout/user", response_model=List[BookingModel])
def checkout_user(
    request: CheckoutUserRequest,
    current_user_id: str = Depends(get_current_user)
):
    """
    Thanh toán từ giỏ hàng - USER ĐÃ ĐĂNG NHẬP
    
    **Yêu cầu:** Bearer Token trong header Authorization
    
    **Luồng:**
    1. Verify token và lấy user_id từ token
    2. Lấy tất cả cart_items từ cart_id
    3. Tạo 1 booking cho mỗi cart_item (gắn user_id từ token)
    4. Tính total_price từ price_snapshot × quantity × (adult + child)
    5. Xóa cart sau khi tạo booking thành công
    
    **Request:**
    ```json
    {
      "cart_id": "uuid",
      "adult_count": 2,
      "child_count": 1,
      "special_request": "Yêu cầu đặc biệt"
    }
    ```
    
    **Headers:**
    ```
    Authorization: Bearer <token>
    ```
    
    **Response:** Danh sách bookings đã tạo
    """
    try:
        checkout_data = request.model_dump()
        checkout_data["user_id"] = uuid.UUID(current_user_id)
        return BookingService.checkout_from_cart(checkout_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout/guest", response_model=List[BookingModel])
def checkout_guest(request: CheckoutGuestRequest):
    """
    Thanh toán từ giỏ hàng - KHÁCH VÃNG LAI
    
    **Luồng:**
    1. Lấy tất cả cart_items từ cart_id
    2. Tạo 1 booking cho mỗi cart_item (gắn session_id)
    3. Lưu thông tin guest (name, phone, email)
    4. Tính total_price từ price_snapshot × quantity × (adult + child)
    5. Xóa cart sau khi tạo booking thành công
    
    **Request:**
    ```json
    {
      "cart_id": "uuid",
      "session_id": "uuid",
      "guest_name": "Nguyễn Văn A",
      "guest_phone": "0123456789",
      "guest_email": "email@example.com",
      "adult_count": 2,
      "child_count": 1,
      "special_request": "Yêu cầu đặc biệt"
    }
    ```
    
    **Response:** Danh sách bookings đã tạo
    """
    try:
        return BookingService.checkout_from_cart(request.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create", response_model=BookingModel)
def create_booking(booking: BookingCreateModel):
    """
    Tạo booking thủ công - Đặt tour trực tiếp (không qua giỏ hàng)
    
    **Lưu ý:** Nên dùng /checkout để tạo booking từ cart
    
    **Request body:**
    - cart_item_id: UUID của cart_item (bắt buộc)
    - user_id: UUID của user (nếu đã đăng nhập)
    - session_id: UUID session (nếu khách vãng lai)
    - tour_id: UUID của tour (bắt buộc)
    - adult_count, child_count: Số lượng người lớn/trẻ em
    - total_price: Tổng giá tour
    - guest_name, guest_phone, guest_email: Thông tin khách
    - special_request: Yêu cầu đặc biệt
    
    **Status mặc định:** pending
    """
    return BookingService.create(booking)


@router.get("/all", response_model=List[BookingModel])
def get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: str = Depends(get_current_admin)
):
    """Lấy danh sách tất cả bookings - Chỉ admin được phép"""
    return BookingService.get_all(skip, limit)


@router.get("/user/{user_id}", response_model=List[BookingModel])
def get_bookings_by_user(
    user_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Lấy danh sách bookings của user"""
    return BookingService.get_by_user_id(user_id, skip, limit)


@router.get("/session/{session_id}", response_model=List[BookingModel])
def get_bookings_by_session(
    session_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Lấy danh sách bookings theo session_id (khách vãng lai)"""
    return BookingService.get_by_session_id(session_id, skip, limit)


@router.get("/tour/{tour_id}", response_model=List[BookingModel])
def get_bookings_by_tour(
    tour_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: str = Depends(get_current_admin)
):
    """Lấy danh sách bookings theo tour_id - Chỉ admin được phép"""
    return BookingService.get_by_tour_id(tour_id, skip, limit)


@router.get("/status/{status}", response_model=List[BookingModel])
def get_bookings_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: str = Depends(get_current_admin)
):
    """Lấy danh sách bookings theo status - Chỉ admin được phép"""
    return BookingService.get_by_status(status, skip, limit)


@router.get("/statistics")
def get_booking_statistics(current_admin: str = Depends(get_current_admin)):
    """Lấy thống kê bookings theo status - Chỉ admin được phép"""
    return BookingService.get_booking_statistics()


@router.get("/chatbot/bookings", response_model=List[BookingWithCartItemModel])
def get_chatbot_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_admin: str = Depends(get_current_admin)
):
    """
    Lấy tất cả bookings từ chatbot kèm cart items - Chỉ admin được phép
    
    Trả về các bookings có metadata['source'] = 'chatbot' 
    kèm theo thông tin chi tiết của cart_item tương ứng
    
    **Response:**
    ```json
    [
      {
        "id": "uuid",
        "user_id": "uuid",
        "tour_id": "uuid",
        "cart_item_id": "uuid",
        "guest_name": "Nguyen Van A",
        "adult_count": 2,
        "child_count": 1,
        "total_price": 15000000,
        "status": "pending",
        "meta_data": {
          "source": "chatbot",
          "chat_id": "uuid",
          "booking_time": "2025-12-10T15:43:59"
        },
        "cart_item": {
          "id": "uuid",
          "cart_id": "uuid",
          "tour_id": "uuid",
          "quantity": 1,
          "price_snapshot": 5000000,
          "travel_date": "2025-12-20"
        },
        "created_at": "2025-12-10T15:43:59",
        "updated_at": "2025-12-10T15:43:59"
      }
    ]
    ```
    """
    return BookingService.get_chatbot_bookings(skip, limit)


@router.get("/{booking_id}", response_model=BookingModel)
def get_booking(booking_id: uuid.UUID):
    """Lấy thông tin chi tiết booking theo ID"""
    booking = BookingService.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/update/{booking_id}", response_model=BookingModel)
def update_booking(
    booking_id: uuid.UUID,
    booking: BookingUpdateModel,
    current_admin: str = Depends(get_current_admin)
):
    """Cập nhật booking - Chỉ admin được phép"""
    updated_booking = BookingService.update(booking_id, booking)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking


@router.patch("/update-status/{booking_id}", response_model=BookingModel)
def update_booking_status(
    booking_id: uuid.UUID,
    status: str = Query(..., description="Status mới: pending/confirmed/cancelled/completed"),
    current_admin: str = Depends(get_current_admin)
):
    """Cập nhật status của booking - Chỉ admin được phép"""
    updated_booking = BookingService.update_status(booking_id, status)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@router.delete("/hard-delete/{booking_id}")
def hard_delete_booking(
    booking_id: uuid.UUID,
    current_admin: str = Depends(get_current_admin)
):
    """Hard delete booking (xóa vĩnh viễn) - Chỉ admin được phép"""
    success = BookingService.hard_delete(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking permanently deleted"}

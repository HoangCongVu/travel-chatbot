import uuid
from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel, Field
from models.payments import PaymentModel, PaymentCreateModel, PaymentUpdateModel
from services.payments import PaymentService
from middleware.auth import get_current_admin

router = APIRouter(prefix="/payments", tags=["Payments"])


class CreatePaymentRequest(BaseModel):
    """Request body để tạo payment cho booking"""
    booking_id: uuid.UUID
    payment_method: str = Field(default="sepay", description="sepay, momo, vnpay, zalopay")
    meta_data: dict | None = None


@router.post("/create-for-booking", response_model=PaymentModel)
def create_payment_for_booking(request: CreatePaymentRequest):
    """
    Tạo payment cho booking
    
    **Tự động:**
    - Lấy amount từ booking.total_price
    - Tạo transaction_id ngẫu nhiên
    - Generate payment_url (mock)
    - Set payment_status = pending
    
    **Request:**
    ```json
    {
      "booking_id": "uuid",
      "payment_method": "sepay"
    }
    ```
    """
    try:
        return PaymentService.create_for_booking(
            booking_id=request.booking_id,
            payment_method=request.payment_method,
            meta_data=request.meta_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/check-status/{payment_id}")
def check_payment_status(payment_id: uuid.UUID):
    """
    Kiểm tra trạng thái thanh toán
    
    **Response:**
    - Nếu payment_status = "success" → Trả về thông báo thành công
    - Nếu payment_status khác → Trả về trạng thái hiện tại
    """
    payment = PaymentService.get(payment_id)
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    status_map = {
        "success": "Thanh toán thành công!",
        "pending": "Đang chờ thanh toán",
        "failed": "Thanh toán thất bại"
    }
    
    message = status_map.get(payment.payment_status, f"Trạng thái: {payment.payment_status}")
    
    # Trả về response đơn giản
    return {
        "payment_id": payment.payment_status,
        "message": message
    }


@router.get("/all", response_model=List[PaymentModel])
def get_all_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: str = Depends(get_current_admin)
):
    """Lấy danh sách tất cả payments - Chỉ admin được phép"""
    return PaymentService.get_all(skip, limit)


@router.get("/booking/{booking_id}", response_model=List[PaymentModel])
def get_payments_by_booking(booking_id: uuid.UUID):
    """Lấy danh sách payments theo booking_id"""
    return PaymentService.get_by_booking_id(booking_id)


@router.get("/status/{payment_status}", response_model=List[PaymentModel])
def get_payments_by_status(
    payment_status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """Lấy danh sách payments theo status - Chỉ admin được phép"""
    return PaymentService.get_by_status(payment_status, skip, limit)


@router.get("/transaction/{transaction_id}", response_model=PaymentModel)
def get_payment_by_transaction(
    transaction_id: str,
    current_admin: str = Depends(get_current_admin)
):
    """Lấy payment theo transaction_id - Chỉ admin được phép"""
    payment = PaymentService.get_by_transaction_id(transaction_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/statistics")
def get_payment_statistics(current_admin: str = Depends(get_current_admin)):
    """Lấy thống kê payments theo status - Chỉ admin được phép"""
    return PaymentService.get_payment_statistics()


@router.get("/total-success-amount")
def get_total_success_amount(current_admin: str = Depends(get_current_admin)):
    """Tính tổng tiền của tất cả payments có status = success - Chỉ admin được phép"""
    total = PaymentService.get_total_success_amount()
    return {
        "status": "success",
        "total_success_amount": total,
        "message": f"Tổng tiền từ các giao dịch thành công: {total:,.0f} VND"
    }


@router.get("/booking/{booking_id}/total")
def get_total_amount_by_booking(
    booking_id: uuid.UUID,
    current_admin: str = Depends(get_current_admin)
):
    """Tính tổng số tiền đã thanh toán cho một booking - Chỉ admin được phép"""
    total = PaymentService.get_total_amount_by_booking(booking_id)
    return {"booking_id": booking_id, "total_paid": total}


@router.get("/{payment_id}", response_model=PaymentModel)
def get_payment(payment_id: uuid.UUID):
    """Lấy thông tin chi tiết payment theo ID"""
    payment = PaymentService.get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/update/{payment_id}", response_model=PaymentModel)
def update_payment(
    payment_id: uuid.UUID,
    payment: PaymentUpdateModel,
    current_admin: str = Depends(get_current_admin)
):
    """Cập nhật payment - Chỉ admin được phép"""
    updated_payment = PaymentService.update(payment_id, payment)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


@router.patch("/update-status/{payment_id}", response_model=PaymentModel)
def update_payment_status(
    payment_id: uuid.UUID,
    payment_status: str = Query(..., description="Status mới: pending/processing/success/failed/refunded"),
    current_admin: str = Depends(get_current_admin)
):
    """Cập nhật status của payment - Chỉ admin được phép"""
    updated_payment = PaymentService.update_status(payment_id, payment_status)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


@router.delete("/{payment_id}")
def delete_payment(
    payment_id: uuid.UUID,
    current_admin: str = Depends(get_current_admin)
):
    """Xóa payment - Chỉ admin được phép"""
    success = PaymentService.delete(payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}

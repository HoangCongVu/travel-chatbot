import uuid
from services.payments import PaymentService
from services.bookings import BookingService
from repositories.payments import PaymentRepository


class PaymentWebhookService:
    """Service xử lý webhook từ payment gateway"""
    
    async def handle_webhook(self, data: dict):
        """
        Xử lý webhook từ SePay hoặc payment gateway khác
        
        **Expected data format:**
        {
            "transaction_id": "SEPAY_ABC123",  # hoặc payment_id
            "status": "success",  # pending/processing/success/failed
            "amount": 17600000,
            "content": "Thanh toan don hang...",
            ...
        }
        """
        # Lấy transaction_id hoặc payment_id từ webhook
        # Sepay gửi: code (mã giao dịch), referenceCode (mã tham chiếu), hoặc transferId
        transaction_id = (
            data.get("transaction_id") or 
            data.get("code") or 
            data.get("referenceCode") or 
            data.get("transferId")
        )
        payment_id = data.get("payment_id")
        
        # Lấy status từ webhook (KHÔNG set default)
        # SePay chỉ gọi webhook khi ĐÃ NHẬN TIỀN THẬT
        # Nhưng vẫn cần check để tránh false positive
        status = data.get("status")
        
        # Nếu không có status field, coi như đây là webhook thông báo nhận tiền từ SePay
        # (SePay mặc định webhook = đã nhận tiền)
        if status is None:
            # Kiểm tra xem có đủ dữ liệu giao dịch không
            has_transaction_data = (
                data.get("amount") and 
                (data.get("transferId") or data.get("code") or data.get("referenceCode"))
            )
            if has_transaction_data:
                status = "success"
            else:
                # Webhook không hợp lệ
                return None
        
        # Map status từ webhook sang hệ thống
        status_mapping = {
            "success": "success",
            "completed": "success",
            "failed": "failed",
            "pending": "pending",
            "processing": "processing"
        }
        payment_status = status_mapping.get(status.lower(), "success")
        
        updated_payment = None
        
        # Cập nhật payment theo transaction_id (ưu tiên)
        if transaction_id:
            updated_payment = PaymentService.update_by_transaction_id(
                transaction_id=transaction_id,
                payment_status=payment_status
            )
        
        # Nếu không tìm thấy bằng transaction_id, thử payment_id
        if not updated_payment and payment_id:
            try:
                payment_uuid = uuid.UUID(payment_id)
                updated_payment = PaymentService.update_payment_status(
                    payment_id=payment_uuid,
                    payment_status=payment_status,
                    transaction_id=transaction_id
                )
            except (ValueError, AttributeError):
                pass
        
        # Nếu payment thành công, cập nhật booking status
        if updated_payment and payment_status == "success":
            booking = BookingService.get(updated_payment.booking_id)
            if booking and booking.status == "pending":
                BookingService.update_status(
                    booking_id=updated_payment.booking_id,
                    status="confirmed"
                )
        
        return updated_payment
    
    def handle_sepay_webhook(self, data: dict):
        """
        Xử lý webhook từ SePay cụ thể
        
        **SePay webhook format:**
        {
            "id": 123456,
            "transferId": "SEPAY_ABC123",
            "transferType": "in",
            "accountNumber": "0123456789",
            "amount": 17600000,
            "content": "Thanh toan booking ABC",
            "when": "2025-12-04 10:00:00"
        }
        """
        # Parse SePay data
        # Sepay có thể gửi: transferId, code, hoặc referenceCode
        transaction_id = (
            data.get("transferId") or 
            data.get("code") or 
            data.get("referenceCode")
        )
        amount = data.get("transferAmount", 0) or data.get("amount", 0)
        content = data.get("content", "")
        
        # Extract booking_id từ content nếu có (VD: "Thanh toan booking {booking_id}")
        # ... logic extract booking_id từ content nếu cần
        
        # Cập nhật payment
        return self.handle_webhook({
            "transaction_id": transaction_id,
            "status": "success",  # SePay webhook là đã nhận tiền
            "amount": amount,
            "meta_data": data
        })

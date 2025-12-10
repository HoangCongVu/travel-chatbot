import uuid
import secrets
from typing import List
from models.payments import PaymentModel, PaymentCreateModel, PaymentUpdateModel
from repositories.payments import PaymentRepository
from repositories.bookings import BookingRepository
from utils.vietqr import generate_vietqr


class PaymentService:
    @staticmethod
    def create_for_booking(
        booking_id: uuid.UUID,
        payment_method: str = "sepay",
        meta_data: dict = None
    ) -> PaymentModel:
        """
        Tạo payment cho booking - Tự động lấy amount từ booking và tạo VietQR
        """
        # Lấy thông tin booking
        booking = BookingRepository.get(booking_id)
        if not booking:
            raise ValueError("Booking không tồn tại")
        
        # Tạo transaction_id theo format SePay: A + 10 ký tự số/chữ
        # VD: A1B2C3D4E5
        random_code = secrets.token_hex(5).upper()  # 10 ký tự hex
        transaction_id = f"AI{random_code}"
        
        # Tạo nội dung chuyển khoản (chỉ chứa mã thanh toán)
        content = transaction_id
        
        # Generate VietQR URL với số tiền và nội dung
        payment_url = generate_vietqr(
            amount=int(booking.total_price),
            content=content
        )
        
        # Tạo payment
        payment_data = PaymentCreateModel(
            booking_id=booking_id,
            amount=booking.total_price,
            payment_method=payment_method,
            payment_status="pending",
            transaction_id=transaction_id,
            payment_url=payment_url,
            meta_data=meta_data or {}
        )
        
        return PaymentRepository.create(payment_data)
    
    @staticmethod
    def create(payload: PaymentCreateModel) -> PaymentModel:
        """Tạo payment mới"""
        return PaymentRepository.create(payload)

    @staticmethod
    def get(payment_id: uuid.UUID) -> PaymentModel | None:
        """Lấy thông tin payment theo ID"""
        return PaymentRepository.get(payment_id)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[PaymentModel]:
        """Lấy danh sách tất cả payments"""
        return PaymentRepository.get_all(skip, limit)

    @staticmethod
    def get_by_booking_id(booking_id: uuid.UUID) -> List[PaymentModel]:
        """Lấy danh sách payments theo booking_id"""
        return PaymentRepository.get_by_booking_id(booking_id)

    @staticmethod
    def get_by_status(payment_status: str, skip: int = 0, limit: int = 100) -> List[PaymentModel]:
        """Lấy danh sách payments theo status"""
        return PaymentRepository.get_by_status(payment_status, skip, limit)

    @staticmethod
    def get_by_transaction_id(transaction_id: str) -> PaymentModel | None:
        """Lấy payment theo transaction_id"""
        return PaymentRepository.get_by_transaction_id(transaction_id)

    @staticmethod
    def update(payment_id: uuid.UUID, payload: PaymentUpdateModel) -> PaymentModel | None:
        """Cập nhật payment"""
        return PaymentRepository.update(payment_id, payload)

    @staticmethod
    def update_status(payment_id: uuid.UUID, payment_status: str) -> PaymentModel | None:
        """Cập nhật status của payment"""
        payload = PaymentUpdateModel(payment_status=payment_status)
        return PaymentRepository.update(payment_id, payload)

    @staticmethod
    def delete(payment_id: uuid.UUID) -> bool:
        """Xóa payment"""
        return PaymentRepository.delete(payment_id)

    @staticmethod
    def count_by_status(payment_status: str) -> int:
        """Đếm số lượng payments theo status"""
        return PaymentRepository.count_by_status(payment_status)

    @staticmethod
    def get_total_amount_by_booking(booking_id: uuid.UUID) -> float:
        """Tính tổng số tiền đã thanh toán cho một booking"""
        return PaymentRepository.get_total_amount_by_booking(booking_id)

    @staticmethod
    def get_total_success_amount() -> float:
        """Tính tổng tiền của tất cả payments có status = success"""
        return PaymentRepository.get_total_success_amount()

    @staticmethod
    def get_payment_statistics() -> dict:
        """Lấy thống kê payments theo status"""
        return {
            "pending": PaymentRepository.count_by_status("pending"),
            "processing": PaymentRepository.count_by_status("processing"),
            "success": PaymentRepository.count_by_status("success"),
            "failed": PaymentRepository.count_by_status("failed"),
            "refunded": PaymentRepository.count_by_status("refunded")
        }

    @staticmethod
    def update_payment_status(
        payment_id: uuid.UUID,
        payment_status: str,
        transaction_id: str = None
    ) -> PaymentModel | None:
        """Cập nhật payment status"""
        return PaymentRepository.update_payment_status(payment_id, payment_status, transaction_id)
    
    @staticmethod
    def update_by_transaction_id(
        transaction_id: str,
        payment_status: str
    ) -> PaymentModel | None:
        """Cập nhật payment status theo transaction_id (webhook)"""
        return PaymentRepository.update_by_transaction_id(transaction_id, payment_status)

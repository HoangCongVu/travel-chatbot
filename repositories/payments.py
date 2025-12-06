import uuid
from typing import List, Optional
from db import Session
from models.payments import PaymentTable, PaymentModel, PaymentCreateModel, PaymentUpdateModel


class PaymentRepository:
    @staticmethod
    def create(payload: PaymentCreateModel) -> PaymentModel:
        """Tạo payment mới"""
        with Session() as session:
            payment = PaymentTable(**payload.model_dump(), id=uuid.uuid4())
            session.add(payment)
            session.commit()
            session.refresh(payment)
            return PaymentModel.model_validate(payment)

    @staticmethod
    def get(payment_id: uuid.UUID) -> PaymentModel | None:
        """Lấy payment theo ID"""
        with Session() as session:
            payment = session.query(PaymentTable).filter(
                PaymentTable.id == payment_id
            ).first()
            return PaymentModel.model_validate(payment) if payment else None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[PaymentModel]:
        """Lấy danh sách tất cả payments"""
        with Session() as session:
            payments = session.query(PaymentTable).offset(skip).limit(limit).all()
            return [PaymentModel.model_validate(payment) for payment in payments]

    @staticmethod
    def get_by_booking_id(booking_id: uuid.UUID) -> List[PaymentModel]:
        """Lấy danh sách payments theo booking_id"""
        with Session() as session:
            payments = session.query(PaymentTable).filter(
                PaymentTable.booking_id == booking_id
            ).all()
            return [PaymentModel.model_validate(payment) for payment in payments]

    @staticmethod
    def get_by_status(payment_status: str, skip: int = 0, limit: int = 100) -> List[PaymentModel]:
        """Lấy danh sách payments theo status"""
        with Session() as session:
            payments = session.query(PaymentTable).filter(
                PaymentTable.payment_status == payment_status
            ).offset(skip).limit(limit).all()
            return [PaymentModel.model_validate(payment) for payment in payments]

    @staticmethod
    def get_by_transaction_id(transaction_id: str) -> PaymentModel | None:
        """Lấy payment theo transaction_id"""
        with Session() as session:
            payment = session.query(PaymentTable).filter(
                PaymentTable.transaction_id == transaction_id
            ).first()
            return PaymentModel.model_validate(payment) if payment else None

    @staticmethod
    def update(payment_id: uuid.UUID, payload: PaymentUpdateModel) -> PaymentModel | None:
        """Cập nhật payment"""
        with Session() as session:
            payment = session.query(PaymentTable).filter(
                PaymentTable.id == payment_id
            ).first()
            if not payment:
                return None
            
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(payment, key, value)
            
            session.commit()
            session.refresh(payment)
            return PaymentModel.model_validate(payment)

    @staticmethod
    def delete(payment_id: uuid.UUID) -> bool:
        """Xóa payment"""
        with Session() as session:
            payment = session.query(PaymentTable).filter(
                PaymentTable.id == payment_id
            ).first()
            if not payment:
                return False
            
            session.delete(payment)
            session.commit()
            return True

    @staticmethod
    def count_by_status(payment_status: str) -> int:
        """Đếm số lượng payments theo status"""
        with Session() as session:
            count = session.query(PaymentTable).filter(
                PaymentTable.payment_status == payment_status
            ).count()
            return count

    @staticmethod
    def update_payment_status(
        payment_id: uuid.UUID, 
        payment_status: str,
        transaction_id: str = None
    ) -> PaymentModel | None:
        """Cập nhật payment status (dùng cho webhook)"""
        with Session() as session:
            payment = session.query(PaymentTable).filter(
                PaymentTable.id == payment_id
            ).first()
            if not payment:
                return None
            
            payment.payment_status = payment_status
            if transaction_id:
                payment.transaction_id = transaction_id
            
            # Nếu status = success, set paid_at
            if payment_status == "success":
                from datetime import datetime, timezone
                payment.paid_at = datetime.now(timezone.utc)
            
            session.commit()
            session.refresh(payment)
            return PaymentModel.model_validate(payment)

    @staticmethod
    def update_by_transaction_id(
        transaction_id: str,
        payment_status: str
    ) -> PaymentModel | None:
        """Cập nhật payment status theo transaction_id (dùng cho webhook)"""
        with Session() as session:
            payment = session.query(PaymentTable).filter(
                PaymentTable.transaction_id == transaction_id
            ).first()
            if not payment:
                return None
            
            payment.payment_status = payment_status
            
            # Nếu status = success, set paid_at
            if payment_status == "success":
                from datetime import datetime, timezone
                payment.paid_at = datetime.now(timezone.utc)
            
            session.commit()
            session.refresh(payment)
            return PaymentModel.model_validate(payment)

    @staticmethod
    def get_total_amount_by_booking(booking_id: uuid.UUID) -> float:
        """Tính tổng số tiền đã thanh toán cho một booking"""
        with Session() as session:
            result = session.query(
                PaymentTable
            ).filter(
                PaymentTable.booking_id == booking_id,
                PaymentTable.payment_status == "success"
            ).all()
            
            total = sum(payment.amount for payment in result)
            return float(total) if total else 0.0

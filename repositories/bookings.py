import uuid
from typing import List, Optional
from datetime import datetime
from db import Session
from models.bookings import BookingTable, BookingModel, BookingCreateModel, BookingUpdateModel
from sqlalchemy import func


class BookingRepository:
    @staticmethod
    def create(payload: BookingCreateModel) -> BookingModel:
        """Tạo booking mới"""
        with Session() as session:
            booking = BookingTable(**payload.model_dump(), id=uuid.uuid4())
            session.add(booking)
            session.commit()
            session.refresh(booking)
            return BookingModel.model_validate(booking)

    @staticmethod
    def get(booking_id: uuid.UUID) -> BookingModel | None:
        """Lấy booking theo ID"""
        with Session() as session:
            booking = session.query(BookingTable).filter(
                BookingTable.id == booking_id,
                BookingTable.deleted_at.is_(None)
            ).first()
            return BookingModel.model_validate(booking) if booking else None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách tất cả bookings"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.deleted_at.is_(None)
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_user_id(user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo user_id"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.user_id == user_id,
                BookingTable.deleted_at.is_(None)
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_session_id(session_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo session_id (khách vãng lai)"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.session_id == session_id,
                BookingTable.deleted_at.is_(None)
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo tour_id"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.tour_id == tour_id,
                BookingTable.deleted_at.is_(None)
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_status(status: str, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo status"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.status == status,
                BookingTable.deleted_at.is_(None)
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def update(booking_id: uuid.UUID, payload: BookingUpdateModel) -> BookingModel | None:
        """Cập nhật booking"""
        with Session() as session:
            booking = session.query(BookingTable).filter(
                BookingTable.id == booking_id,
                BookingTable.deleted_at.is_(None)
            ).first()
            if not booking:
                return None
            
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(booking, key, value)
            
            session.commit()
            session.refresh(booking)
            return BookingModel.model_validate(booking)

    @staticmethod
    def delete(booking_id: uuid.UUID) -> bool:
        """Soft delete booking"""
        with Session() as session:
            booking = session.query(BookingTable).filter(
                BookingTable.id == booking_id,
                BookingTable.deleted_at.is_(None)
            ).first()
            if not booking:
                return False
            
            booking.deleted_at = func.now()
            session.commit()
            return True

    @staticmethod
    def hard_delete(booking_id: uuid.UUID) -> bool:
        """Hard delete booking (xóa vĩnh viễn)"""
        with Session() as session:
            booking = session.query(BookingTable).filter(
                BookingTable.id == booking_id
            ).first()
            if not booking:
                return False
            
            session.delete(booking)
            session.commit()
            return True

    @staticmethod
    def count_by_status(status: str) -> int:
        """Đếm số lượng bookings theo status"""
        with Session() as session:
            count = session.query(BookingTable).filter(
                BookingTable.status == status,
                BookingTable.deleted_at.is_(None)
            ).count()
            return count

    @staticmethod
    def count_by_tour_id(tour_id: uuid.UUID) -> int:
        """Đếm số lượng bookings theo tour_id"""
        with Session() as session:
            count = session.query(BookingTable).filter(
                BookingTable.tour_id == tour_id,
                BookingTable.deleted_at.is_(None)
            ).count()
            return count

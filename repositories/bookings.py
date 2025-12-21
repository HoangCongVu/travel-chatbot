import uuid
from typing import List, Optional
from datetime import datetime
from db import Session
from models.bookings import BookingTable, BookingModel, BookingCreateModel, BookingUpdateModel, BookingWithCartItemModel
from models.cart_items import CartItemTable
from models.tour import TourTable
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
                BookingTable.id == booking_id
            ).first()
            return BookingModel.model_validate(booking) if booking else None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách tất cả bookings"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_user_id(user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo user_id"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.user_id == user_id,
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_session_id(session_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo session_id (khách vãng lai)"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.session_id == session_id
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo tour_id"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.tour_id == tour_id
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_by_status(status: str, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo status"""
        with Session() as session:
            bookings = session.query(BookingTable).filter(
                BookingTable.status == status,
            ).offset(skip).limit(limit).all()
            return [BookingModel.model_validate(booking) for booking in bookings]

    @staticmethod
    def update(booking_id: uuid.UUID, payload: BookingUpdateModel) -> BookingModel | None:
        """Cập nhật booking"""
        with Session() as session:
            booking = session.query(BookingTable).filter(
                BookingTable.id == booking_id
            ).first()
            if not booking:
                return None
            
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(booking, key, value)
            
            session.commit()
            session.refresh(booking)
            return BookingModel.model_validate(booking)


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
                BookingTable.status == status         
            ).count()
            return count

    @staticmethod
    def count_by_tour_id(tour_id: uuid.UUID) -> int:
        """Đếm số lượng bookings theo tour_id"""
        with Session() as session:
            count = session.query(BookingTable).filter(
                BookingTable.tour_id == tour_id
            ).count()
            return count

    @staticmethod
    def get_chatbot_bookings(skip: int = 0, limit: int = 100) -> List[BookingWithCartItemModel]:
        """Lấy tất cả bookings có source từ chatbot và kèm cart_item"""
        with Session() as session:
            bookings = session.query(BookingTable, CartItemTable, TourTable).join(
                CartItemTable,
                BookingTable.cart_item_id == CartItemTable.id
            ).join(
                TourTable,
                CartItemTable.tour_id == TourTable.id
            ).filter(
                BookingTable.meta_data['source'].astext == 'chatbot',
            ).offset(skip).limit(limit).all()
            
            result = []
            for booking, cart_item, tour in bookings:
                booking_dict = BookingModel.model_validate(booking).model_dump()
                booking_dict['tour_name'] = tour.tour_name
                booking_dict['cart_item'] = {
                    'id': cart_item.id,
                    'cart_id': cart_item.cart_id,
                    'tour_name': tour.tour_name,
                    'quantity': cart_item.quantity,
                    'price_snapshot': float(cart_item.price_snapshot),
                    'travel_date': cart_item.travel_date
                }
                result.append(BookingWithCartItemModel(**booking_dict))
            
            return result


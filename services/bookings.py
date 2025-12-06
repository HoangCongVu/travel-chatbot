import uuid
from typing import List, Optional
from models.bookings import BookingModel, BookingCreateModel, BookingUpdateModel
from repositories.bookings import BookingRepository
from repositories.cart_items import CartItemRepository
from repositories.carts import CartRepository


class BookingService:
    @staticmethod
    def checkout_from_cart(checkout_data: dict) -> List[BookingModel]:
        """
        Thanh toán từ giỏ hàng - Tạo bookings cho tất cả items trong cart
        """
        cart_id = checkout_data.get("cart_id")
        if not cart_id:
            raise ValueError("cart_id là bắt buộc")
        
        # Lấy tất cả items trong cart
        cart_items = CartItemRepository.get_by_cart_id(cart_id)
        if not cart_items:
            raise ValueError("Giỏ hàng rỗng")
        
        # Tạo booking cho mỗi cart_item
        bookings = []
        for item in cart_items:
            # Tính total_price = price_snapshot * quantity * (adult + child)
            total_people = checkout_data.get("adult_count", 1) + checkout_data.get("child_count", 0)
            total_price = float(item.price_snapshot) * item.quantity * total_people
            
            booking_data = BookingCreateModel(
                user_id=checkout_data.get("user_id"),
                session_id=checkout_data.get("session_id"),
                tour_id=item.tour_id,
                cart_item_id=item.id,
                guest_name=checkout_data.get("guest_name"),
                guest_phone=checkout_data.get("guest_phone"),
                guest_email=checkout_data.get("guest_email"),
                adult_count=checkout_data.get("adult_count", 1),
                child_count=checkout_data.get("child_count", 0),
                total_price=total_price,
                status="pending",
                special_request=checkout_data.get("special_request"),
                meta_data=checkout_data.get("meta_data")
            )
            booking = BookingRepository.create(booking_data)
            bookings.append(booking)
        
        # KHÔNG xóa cart - giữ lại để tra cứu lịch sử
        # Cart sẽ được xóa thủ công hoặc bởi scheduled task
        # CartRepository.delete(cart_id)
        
        return bookings
    
    @staticmethod
    def create(payload: BookingCreateModel) -> BookingModel:
        """Tạo booking mới"""
        return BookingRepository.create(payload)

    @staticmethod
    def get(booking_id: uuid.UUID) -> BookingModel | None:
        """Lấy thông tin booking theo ID"""
        return BookingRepository.get(booking_id)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách tất cả bookings"""
        return BookingRepository.get_all(skip, limit)

    @staticmethod
    def get_by_user_id(user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo user_id"""
        return BookingRepository.get_by_user_id(user_id, skip, limit)

    @staticmethod
    def get_by_session_id(session_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo session_id (khách vãng lai)"""
        return BookingRepository.get_by_session_id(session_id, skip, limit)

    @staticmethod
    def get_by_tour_id(tour_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo tour_id"""
        return BookingRepository.get_by_tour_id(tour_id, skip, limit)

    @staticmethod
    def get_by_status(status: str, skip: int = 0, limit: int = 100) -> List[BookingModel]:
        """Lấy danh sách bookings theo status"""
        return BookingRepository.get_by_status(status, skip, limit)

    @staticmethod
    def update(booking_id: uuid.UUID, payload: BookingUpdateModel) -> BookingModel | None:
        """Cập nhật booking"""
        return BookingRepository.update(booking_id, payload)

    @staticmethod
    def update_status(booking_id: uuid.UUID, status: str) -> BookingModel | None:
        """Cập nhật status của booking"""
        payload = BookingUpdateModel(status=status)
        return BookingRepository.update(booking_id, payload)

    @staticmethod
    def delete(booking_id: uuid.UUID) -> bool:
        """Soft delete booking"""
        return BookingRepository.delete(booking_id)

    @staticmethod
    def hard_delete(booking_id: uuid.UUID) -> bool:
        """Hard delete booking (xóa vĩnh viễn)"""
        return BookingRepository.hard_delete(booking_id)

    @staticmethod
    def count_by_status(status: str) -> int:
        """Đếm số lượng bookings theo status"""
        return BookingRepository.count_by_status(status)

    @staticmethod
    def count_by_tour_id(tour_id: uuid.UUID) -> int:
        """Đếm số lượng bookings theo tour_id"""
        return BookingRepository.count_by_tour_id(tour_id)

    @staticmethod
    def get_booking_statistics() -> dict:
        """Lấy thống kê bookings theo status"""
        return {
            "pending": BookingRepository.count_by_status("pending"),
            "confirmed": BookingRepository.count_by_status("confirmed"),
            "cancelled": BookingRepository.count_by_status("cancelled"),
            "completed": BookingRepository.count_by_status("completed")
        }

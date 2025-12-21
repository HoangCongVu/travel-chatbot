"""
Service xử lý booking từ chatbot - Quick Booking Tool
"""
import uuid
from datetime import date, datetime
from models.bookings import BookingCreateModel, BookingModel
from models.cart_items import CartItemCreateModel, CartItemModel
from models.carts import CartCreateModel, CartModel
from services.bookings import BookingService
from services.cart_items import CartItemService
from services.carts import CartService
from services.tour import TourService
from utils.context import ChatContext


class ChatbotBookingService:
    """Service xử lý booking trực tiếp từ chatbot"""
    
    @staticmethod
    def quick_book_tour(
        chat_id: str = None,  # UUID string
        user_id: str = None,  # UUID string
        session_id: str = None,  # UUID string
        tour_id: str = None,  # UUID string
        tour_name: str = None,
        travel_date: str = None,
        adult_count: int = 1,
        child_count: int = 0,
        guest_name: str = None,
        guest_phone: str = None,
        guest_email: str = None,
        special_request: str = None
    ) -> dict:
        """
        Đặt tour nhanh từ chatbot
        
        Args:
            chat_id: ID cuộc chat (hoặc lấy từ environment)
            user_id: ID user nếu đã đăng nhập (hoặc lấy từ environment)
            session_id: Session ID nếu khách vãng lai (hoặc lấy từ environment)
            tour_id: ID tour muốn đặt
            tour_name: Tên tour (để tìm nếu không có tour_id)
            travel_date: Ngày khởi hành (YYYY-MM-DD)
            adult_count: Số người lớn
            child_count: Số trẻ em
            guest_name: Tên khách (nếu khách vãng lai)
            guest_phone: SĐT khách
            guest_email: Email khách
            special_request: Yêu cầu đặc biệt
            
        Returns:
            Dict chứa thông tin booking hoặc lỗi
        """
        try:
            # 🔧 AUTO-DETECT context từ ContextVar (thread-safe)
            if not chat_id:
                chat_id = ChatContext.get_chat_id()
            if not user_id:
                user_id = ChatContext.get_user_id()
            if not session_id:
                session_id = ChatContext.get_session_id()
            
            # Convert string UUIDs to UUID objects
            if chat_id:
                chat_uuid = uuid.UUID(chat_id)
            else:
                return {
                    "status": "error",
                    "message": "Không xác định được cuộc trò chuyện"
                }
            
            user_uuid = uuid.UUID(user_id) if user_id else None
            session_uuid = uuid.UUID(session_id) if session_id else None
            tour_uuid = uuid.UUID(tour_id) if tour_id else None
            
            # 1. VALIDATION
            if not tour_uuid and not tour_name:
                return {
                    "status": "error",
                    "message": "Cần tour_id hoặc tour_name để đặt tour"
                }
            
            if not user_uuid and not session_uuid:
                return {
                    "status": "error", 
                    "message": "Cần user_id hoặc session_id để đặt tour"
                }
            
            if not guest_phone:
                return {
                    "status": "error",
                    "message": "Số điện thoại là bắt buộc để đặt tour"
                }
            
            # 2. TÌM TOUR NẾU CHƯA CÓ TOUR_ID
            if not tour_uuid and tour_name:
                tours = TourService.search_by_text(query=tour_name, limit=1)
                # ⚠️ search_by_text trả về LIST object, KHÔNG phải dict
                if not tours or len(tours) == 0:
                    return {
                        "status": "error",
                        "message": f"Không tìm thấy tour '{tour_name}'"
                    }
                # Lấy trực tiếp từ object trong list
                tour_uuid = uuid.UUID(str(tours[0].id))
            
            # 3. LẤY THÔNG TIN CHI TIẾT TOUR
            tour_detail = TourService.get(tour_uuid)
            if not tour_detail or not tour_detail.get("tours"):
                return {
                    "status": "error",
                    "message": f"Không tìm thấy thông tin tour"
                }
            
            # Lấy tour đầu tiên từ danh sách
            tour_info = tour_detail["tours"][0]
            
            # 4. KIỂM TRA PRICE_TYPE - CẤM ĐẶT TOUR "THEO YÊU CẦU"
            price_type = tour_info.get("price_type", "").lower()
            if "theo yêu cầu" in price_type or "on request" in price_type or "liên hệ" in price_type:
                return {
                    "status": "error",
                    "message": f"Tour '{tour_info['tour_name']}' có giá theo yêu cầu. Vui lòng liên hệ hotline 1900 1369 hoặc để lại thông tin, nhân viên sẽ tư vấn chi tiết.",
                    "tour_info": {
                        "tour_name": tour_info["tour_name"],
                        "price_type": tour_info.get("price_type"),
                        "needs_quotation": True
                    }
                }
            
            # 5. TÍNH GIÁ TOUR
            tour_price = ChatbotBookingService._calculate_tour_price(
                tour_info, travel_date, adult_count, child_count
            )
            
            # 6. TẠO CART ITEM (TEMP)
            # Tạo cart tạm để tuân thủ cấu trúc hiện có
            temp_cart = CartService.create(CartCreateModel(
                user_id=user_uuid,
                session_id=session_uuid
            ))
            
            cart_item = CartItemService.create(CartItemCreateModel(
                cart_id=temp_cart.id,
                tour_id=tour_uuid,
                quantity=1,  # 1 booking
                price_snapshot=tour_price,
                travel_date=date.fromisoformat(travel_date) if travel_date else date.today()
            ))
            
            # 7. TẠO BOOKING
            booking_data = BookingCreateModel(
                user_id=user_uuid,
                session_id=session_uuid,
                tour_id=tour_uuid,
                cart_item_id=cart_item.id,
                guest_name=guest_name,
                guest_phone=guest_phone,
                guest_email=guest_email,
                adult_count=adult_count,
                child_count=child_count,
                total_price=tour_price,
                status="pending",
                special_request=special_request,
                meta_data={
                    "source": "chatbot",
                    "chat_id": str(chat_uuid),
                    "booking_time": datetime.now().isoformat()
                }
            )
            
            booking = BookingService.create(booking_data)
            
            return {
                "status": "success",
                "message": "Đặt tour thành công!",
                "data": {
                    "booking_id": str(booking.id),
                    "tour_name": tour_info["tour_name"],
                    "total_price": tour_price,
                    "adult_count": adult_count,
                    "child_count": child_count,
                    "travel_date": travel_date,
                    "status": booking.status,
                    "guest_info": {
                        "name": guest_name,
                        "phone": guest_phone,
                        "email": guest_email
                    } if guest_name else None
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Lỗi khi đặt tour: {str(e)}"
            }
    
    @staticmethod
    def _calculate_tour_price(tour_info: dict, travel_date: str = None, adult_count: int = 1, child_count: int = 0) -> float:
        """
        Tính giá tour dựa trên thông tin chi tiết
        
        Args:
            tour_info: Thông tin tour từ TourService.get()["tours"][0]
            travel_date: Ngày khởi hành
            adult_count: Số người lớn
            child_count: Số trẻ em
            
        Returns:
            Tổng giá tour
        """
        try:
            # Lấy giá cơ bản
            base_price = 0
            
            # 1. Ưu tiên price_by_dates nếu có travel_date
            if travel_date and tour_info.get("price_by_dates"):
                for price_date in tour_info["price_by_dates"]:
                    if price_date.get("date") == travel_date:
                        base_price = float(price_date["price"])
                        break
            
            # 2. Nếu chưa có giá, dùng price_by_packages
            if base_price == 0 and tour_info.get("price_by_packages"):
                # Lấy giá package đầu tiên hoặc package "Standard"
                for package in tour_info["price_by_packages"]:
                    if package.get("package_name", "").lower() in ["standard", "cơ bản", "thường"]:
                        base_price = float(package["price"])
                        break
                
                # Nếu không có package standard, lấy giá đầu tiên
                if base_price == 0:
                    base_price = float(tour_info["price_by_packages"][0]["price"])
            
            # 3. Nếu vẫn không có giá → LỖI (KHÔNG dùng giá mặc định)
            if base_price == 0:
                raise ValueError("Không tìm thấy giá tour hợp lệ")
            
            # 4. Tính giá cho trẻ em (thường 70% giá người lớn)
            child_price = base_price * 0.7
            
            # 5. Tổng giá
            total_price = (base_price * adult_count) + (child_price * child_count)
            
            return total_price
            
        except Exception as e:
            print(f"⚠️ Lỗi tính giá tour: {str(e)}")
            raise  # Throw lỗi lên trên thay vì return giá mặc định
    
    @staticmethod
    def get_user_bookings(user_id: uuid.UUID = None, session_id: uuid.UUID = None, limit: int = 5) -> dict:
        """
        Lấy danh sách booking của user
        
        Args:
            user_id: ID user (nếu đã đăng nhập)
            session_id: Session ID (nếu khách vãng lai)
            limit: Số booking tối đa
            
        Returns:
            Dict chứa danh sách booking
        """
        try:
            if user_id:
                bookings = BookingService.get_by_user_id(user_id, limit=limit)
            elif session_id:
                bookings = BookingService.get_by_session_id(session_id, limit=limit)
            else:
                return {
                    "status": "error",
                    "message": "Cần user_id hoặc session_id để lấy danh sách booking"
                }
            
            return {
                "status": "success", 
                "data": {
                    "bookings": [
                        {
                            "booking_id": str(booking.id),
                            "tour_id": str(booking.tour_id),
                            "adult_count": booking.adult_count,
                            "child_count": booking.child_count,
                            "total_price": booking.total_price,
                            "status": booking.status,
                            "created_at": booking.created_at.isoformat(),
                            "guest_name": booking.guest_name
                        }
                        for booking in bookings
                    ],
                    "total_found": len(bookings)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Lỗi khi lấy danh sách booking: {str(e)}"
            }
    
    @staticmethod  
    def cancel_booking(booking_id: uuid.UUID, user_id: uuid.UUID = None, session_id: uuid.UUID = None) -> dict:
        """
        Hủy booking
        
        Args:
            booking_id: ID booking cần hủy
            user_id: ID user (để verify quyền hủy)
            session_id: Session ID (để verify quyền hủy)
            
        Returns:
            Dict kết quả hủy booking
        """
        try:
            # 1. Kiểm tra booking tồn tại
            booking = BookingService.get(booking_id)
            if not booking:
                return {
                    "status": "error",
                    "message": "Không tìm thấy booking"
                }
            
            # 2. Verify quyền hủy
            if user_id and booking.user_id != user_id:
                return {
                    "status": "error", 
                    "message": "Bạn không có quyền hủy booking này"
                }
            
            if session_id and booking.session_id != session_id:
                return {
                    "status": "error",
                    "message": "Bạn không có quyền hủy booking này"
                }
            
            # 3. Chỉ cho phép hủy booking pending
            if booking.status not in ["pending"]:
                return {
                    "status": "error",
                    "message": f"Không thể hủy booking với status '{booking.status}'"
                }
            
            # 4. Cập nhật status thành cancelled
            updated_booking = BookingService.update_status(booking_id, "cancelled")
            
            return {
                "status": "success",
                "message": "Hủy booking thành công!",
                "data": {
                    "booking_id": str(updated_booking.id),
                    "status": updated_booking.status,
                    "cancelled_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Lỗi khi hủy booking: {str(e)}"
            }
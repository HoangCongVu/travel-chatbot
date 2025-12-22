import uuid
from typing import List
from datetime import date
from models.cart_items import CartItemModel, CartItemCreateModel, CartItemUpdateModel
from repositories.cart_items import CartItemRepository
from repositories.carts import CartRepository
from repositories.tour import TourRepository
from repositories.price_by_date import PriceByDateRepository
from repositories.price_by_package import PriceByPackageRepository


class CartItemService:
    @staticmethod
    def create(payload: CartItemCreateModel) -> CartItemModel:
        """Thêm item vào cart"""
        return CartItemRepository.create(payload)

    @staticmethod
    def add_to_cart(
        cart_id: uuid.UUID,
        tour_id: uuid.UUID,
        travel_date: date,
        quantity: int = 1
    ) -> CartItemModel:
        """
        Thêm tour vào giỏ hàng - Tự động tính giá
        Nếu item đã tồn tại thì cập nhật số lượng
        """
        # Kiểm tra tour có tồn tại không
        tour = TourRepository.get(tour_id)
        if not tour:
            raise ValueError("Tour không tồn tại")

        # Tính giá dựa vào price_type
        price = 0.0
        
        # Danh sách các price_type dựa trên ngày
        date_based_types = [
            "by_date",
            "Dựa trên ngày khởi hành quốc tế",
            "Dựa trên mùa – theo ngày",
            "Dựa trên ngày cao điểm",
            "Dựa trên ngày bay"
        ]
        
        # Danh sách các price_type dựa trên gói
        package_based_types = [
            "by_package",
            "Dựa trên gói",
            "Cố định"
        ]
        
        if tour.price_type in date_based_types:
            # Giá theo ngày cụ thể - tìm trong price_by_dates
            price_by_date = PriceByDateRepository.get_by_tour_and_date(tour_id, travel_date)
            if price_by_date:
                price = float(price_by_date.price)
            else:
                # Nếu không tìm thấy giá theo ngày, thử lấy giá từ package
                packages = PriceByPackageRepository.get_by_tour_id(tour_id)
                if packages:
                    price = float(packages[0].price)
                else:
                    raise ValueError(f"Không tìm thấy giá cho tour này vào ngày {travel_date}")
        elif tour.price_type in package_based_types:
            # Giá theo gói hoặc cố định
            packages = PriceByPackageRepository.get_by_tour_id(tour_id)
            if packages:
                price = float(packages[0].price)
            else:
                raise ValueError(f"Không tìm thấy gói giá cho tour này")
        elif tour.price_type == "Theo yêu cầu":
            # Tour theo yêu cầu - giá mặc định là 0, cần liên hệ
            raise ValueError(f"Tour '{tour.tour_name}' là tour theo yêu cầu. Vui lòng liên hệ để được báo giá.")
        else:
            # Fallback: thử tìm giá trong cả 2 bảng
            price_by_date = PriceByDateRepository.get_by_tour_and_date(tour_id, travel_date)
            if price_by_date:
                price = float(price_by_date.price)
            else:
                packages = PriceByPackageRepository.get_by_tour_id(tour_id)
                if packages:
                    price = float(packages[0].price)
                else:
                    raise ValueError(f"Không tìm thấy giá cho tour này (price_type: {tour.price_type})")

        # Kiểm tra item đã tồn tại chưa
        existing_item = CartItemRepository.get_by_cart_and_tour(cart_id, tour_id, travel_date)
        
        if existing_item:
            # Cập nhật số lượng
            updated_item = CartItemRepository.update(
                existing_item.id,
                CartItemUpdateModel(quantity=existing_item.quantity + quantity)
            )
            # Thêm tour_name vào response
            if updated_item:
                updated_item.tour_name = tour.tour_name
            return updated_item
        else:
            # Tạo mới
            new_item = CartItemCreateModel(
                cart_id=cart_id,
                tour_id=tour_id,
                quantity=quantity,
                price_snapshot=price,
                travel_date=travel_date
            )
            created_item = CartItemRepository.create(new_item)
            # Thêm tour_name vào response
            if created_item:
                created_item.tour_name = tour.tour_name
            return created_item

    @staticmethod
    def get(cart_item_id: uuid.UUID) -> CartItemModel | None:
        """Lấy cart item theo ID"""
        return CartItemRepository.get(cart_item_id)

    @staticmethod
    def get_by_cart_id(cart_id: uuid.UUID) -> List[CartItemModel]:
        """Lấy tất cả items trong cart với thông tin tour"""
        items = CartItemRepository.get_by_cart_id(cart_id)
        # Thêm tour_name cho mỗi item
        for item in items:
            tour = TourRepository.get(item.tour_id)
            if tour:
                item.tour_name = tour.tour_name
        return items

    @staticmethod
    def update(cart_item_id: uuid.UUID, payload: CartItemUpdateModel) -> CartItemModel | None:
        """Cập nhật cart item"""
        return CartItemRepository.update(cart_item_id, payload)

    @staticmethod
    def update_quantity(cart_item_id: uuid.UUID, quantity: int) -> CartItemModel | None:
        """Cập nhật số lượng"""
        return CartItemRepository.update(
            cart_item_id,
            CartItemUpdateModel(quantity=quantity)
        )

    @staticmethod
    def delete(cart_item_id: uuid.UUID) -> bool:
        """Xóa item khỏi cart"""
        return CartItemRepository.delete(cart_item_id)

    @staticmethod
    def clear_cart(cart_id: uuid.UUID) -> bool:
        """Xóa tất cả items trong cart"""
        return CartItemRepository.delete_by_cart_id(cart_id)

    @staticmethod
    def get_cart_total(cart_id: uuid.UUID) -> float:
        """Tính tổng giá trị giỏ hàng"""
        items = CartItemRepository.get_by_cart_id(cart_id)
        total = sum(item.price_snapshot * item.quantity for item in items)
        return float(total)

    @staticmethod
    def get_cart_count(cart_id: uuid.UUID) -> int:
        """Đếm số lượng items trong cart"""
        return CartItemRepository.count_by_cart_id(cart_id)

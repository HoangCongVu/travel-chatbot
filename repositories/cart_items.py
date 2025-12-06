import uuid
from typing import List
from db import Session
from models.cart_items import CartItemTable, CartItemModel, CartItemCreateModel, CartItemUpdateModel


class CartItemRepository:
    @staticmethod
    def create(payload: CartItemCreateModel) -> CartItemModel:
        """Tạo cart item mới"""
        with Session() as session:
            cart_item = CartItemTable(**payload.model_dump(), id=uuid.uuid4())
            session.add(cart_item)
            session.commit()
            session.refresh(cart_item)
            return CartItemModel.model_validate(cart_item)

    @staticmethod
    def get(cart_item_id: uuid.UUID) -> CartItemModel | None:
        """Lấy cart item theo ID"""
        with Session() as session:
            item = session.query(CartItemTable).filter(CartItemTable.id == cart_item_id).first()
            return CartItemModel.model_validate(item) if item else None

    @staticmethod
    def get_by_cart_id(cart_id: uuid.UUID) -> List[CartItemModel]:
        """Lấy tất cả items trong cart"""
        with Session() as session:
            items = session.query(CartItemTable).filter(
                CartItemTable.cart_id == cart_id
            ).all()
            return [CartItemModel.model_validate(item) for item in items]

    @staticmethod
    def get_by_cart_and_tour(cart_id: uuid.UUID, tour_id: uuid.UUID, travel_date) -> CartItemModel | None:
        """Kiểm tra item đã tồn tại trong cart chưa"""
        with Session() as session:
            item = session.query(CartItemTable).filter(
                CartItemTable.cart_id == cart_id,
                CartItemTable.tour_id == tour_id,
                CartItemTable.travel_date == travel_date
            ).first()
            return CartItemModel.model_validate(item) if item else None

    @staticmethod
    def update(cart_item_id: uuid.UUID, payload: CartItemUpdateModel) -> CartItemModel | None:
        """Cập nhật cart item"""
        with Session() as session:
            item = session.query(CartItemTable).filter(CartItemTable.id == cart_item_id).first()
            if not item:
                return None
            
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(item, key, value)
            
            session.commit()
            session.refresh(item)
            return CartItemModel.model_validate(item)

    @staticmethod
    def delete(cart_item_id: uuid.UUID) -> bool:
        """Xóa cart item"""
        with Session() as session:
            item = session.query(CartItemTable).filter(CartItemTable.id == cart_item_id).first()
            if not item:
                return False
            
            session.delete(item)
            session.commit()
            return True

    @staticmethod
    def delete_by_cart_id(cart_id: uuid.UUID) -> bool:
        """Xóa tất cả items trong cart (clear cart)"""
        with Session() as session:
            session.query(CartItemTable).filter(
                CartItemTable.cart_id == cart_id
            ).delete()
            session.commit()
            return True

    @staticmethod
    def count_by_cart_id(cart_id: uuid.UUID) -> int:
        """Đếm số lượng items trong cart"""
        with Session() as session:
            count = session.query(CartItemTable).filter(
                CartItemTable.cart_id == cart_id
            ).count()
            return count

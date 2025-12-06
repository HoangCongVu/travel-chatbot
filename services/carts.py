import uuid
from typing import List
from models.carts import CartModel, CartCreateModel, CartUpdateModel
from repositories.carts import CartRepository


class CartService:
    @staticmethod
    def create(payload: CartCreateModel) -> CartModel:
        """Tạo cart mới"""
        return CartRepository.create(payload)

    @staticmethod
    def get(cart_id: uuid.UUID) -> CartModel | None:
        """Lấy cart theo ID"""
        return CartRepository.get(cart_id)

    @staticmethod
    def get_by_user_id(user_id: uuid.UUID) -> CartModel | None:
        """Lấy cart của user"""
        return CartRepository.get_by_user_id(user_id)

    @staticmethod
    def get_by_session_id(session_id: uuid.UUID) -> CartModel | None:
        """Lấy cart theo session (khách vãng lai)"""
        return CartRepository.get_by_session_id(session_id)

    @staticmethod
    def get_or_create_by_user(user_id: uuid.UUID) -> CartModel:
        """Lấy hoặc tạo cart cho user"""
        return CartRepository.get_or_create_by_user(user_id)

    @staticmethod
    def get_or_create_by_session(session_id: uuid.UUID) -> CartModel:
        """Lấy hoặc tạo cart cho session"""
        return CartRepository.get_or_create_by_session(session_id)

    @staticmethod
    def update(cart_id: uuid.UUID, payload: CartUpdateModel) -> CartModel | None:
        """Cập nhật cart"""
        return CartRepository.update(cart_id, payload)

    @staticmethod
    def delete(cart_id: uuid.UUID) -> bool:
        """Xóa cart"""
        return CartRepository.delete(cart_id)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[CartModel]:
        """Lấy danh sách tất cả carts"""
        return CartRepository.get_all(skip, limit)

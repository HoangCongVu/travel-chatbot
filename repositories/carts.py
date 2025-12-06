import uuid
from typing import List, Optional
from db import Session
from models.carts import CartTable, CartModel, CartCreateModel, CartUpdateModel


class CartRepository:
    @staticmethod
    def create(payload: CartCreateModel) -> CartModel:
        """Tạo cart mới"""
        with Session() as session:
            cart = CartTable(**payload.model_dump(), id=uuid.uuid4())
            session.add(cart)
            session.commit()
            session.refresh(cart)
            return CartModel.model_validate(cart)

    @staticmethod
    def get(cart_id: uuid.UUID) -> CartModel | None:
        """Lấy cart theo ID"""
        with Session() as session:
            cart = session.query(CartTable).filter(CartTable.id == cart_id).first()
            return CartModel.model_validate(cart) if cart else None

    @staticmethod
    def get_by_user_id(user_id: uuid.UUID) -> CartModel | None:
        """Lấy cart theo user_id"""
        with Session() as session:
            cart = session.query(CartTable).filter(
                CartTable.user_id == user_id
            ).first()
            return CartModel.model_validate(cart) if cart else None

    @staticmethod
    def get_by_session_id(session_id: uuid.UUID) -> CartModel | None:
        """Lấy cart theo session_id (cho khách vãng lai)"""
        with Session() as session:
            cart = session.query(CartTable).filter(
                CartTable.session_id == session_id
            ).first()
            return CartModel.model_validate(cart) if cart else None

    @staticmethod
    def get_or_create_by_user(user_id: uuid.UUID) -> CartModel:
        """Lấy hoặc tạo cart cho user"""
        cart = CartRepository.get_by_user_id(user_id)
        if not cart:
            cart = CartRepository.create(CartCreateModel(user_id=user_id))
        return cart

    @staticmethod
    def get_or_create_by_session(session_id: uuid.UUID) -> CartModel:
        """Lấy hoặc tạo cart cho session (khách vãng lai)"""
        cart = CartRepository.get_by_session_id(session_id)
        if not cart:
            cart = CartRepository.create(CartCreateModel(session_id=session_id))
        return cart

    @staticmethod
    def update(cart_id: uuid.UUID, payload: CartUpdateModel) -> CartModel | None:
        """Cập nhật cart"""
        with Session() as session:
            cart = session.query(CartTable).filter(CartTable.id == cart_id).first()
            if not cart:
                return None
            
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(cart, key, value)
            
            session.commit()
            session.refresh(cart)
            return CartModel.model_validate(cart)

    @staticmethod
    def delete(cart_id: uuid.UUID) -> bool:
        """Xóa cart"""
        with Session() as session:
            cart = session.query(CartTable).filter(CartTable.id == cart_id).first()
            if not cart:
                return False
            
            session.delete(cart)
            session.commit()
            return True

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[CartModel]:
        """Lấy danh sách tất cả carts"""
        with Session() as session:
            carts = session.query(CartTable).offset(skip).limit(limit).all()
            return [CartModel.model_validate(cart) for cart in carts]

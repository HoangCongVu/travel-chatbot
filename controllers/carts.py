import uuid
from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException
from models.carts import CartModel, CartCreateModel, CartUpdateModel
from services.carts import CartService
from middleware.auth import get_current_admin, get_current_user

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("/create/user", response_model=CartModel)
def create_cart_for_user(current_user_id: str = Depends(get_current_user)):
    """
    Tạo giỏ hàng cho user đã đăng nhập
    
    """
    return CartService.create(CartCreateModel(user_id=uuid.UUID(current_user_id)))


@router.post("/create/guest", response_model=CartModel)
def create_cart_for_guest():
    """
    Tạo giỏ hàng cho khách vãng lai
    
    Tự động tạo session_id ngẫu nhiên và trả về
    """
    session_id = str(uuid.uuid4())
    return CartService.create(CartCreateModel(session_id=session_id))


@router.post("/create", response_model=CartModel)
def create_cart(cart: CartCreateModel):
    """
    Tạo cart mới (API thủ công)
    - Cho user đăng nhập: gửi user_id
    - Cho khách vãng lai: gửi session_id
    """
    return CartService.create(cart)


@router.get("/user/me", response_model=CartModel)
def get_my_cart(current_user_id: str = Depends(get_current_user)):
    """
    Lấy giỏ hàng của user hiện tại (từ token)
    
    **Yêu cầu:** Bearer Token trong header Authorization
    """
    cart = CartService.get_by_user_id(uuid.UUID(current_user_id))
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/user/{user_id}", response_model=CartModel)
def get_cart_by_user(user_id: uuid.UUID):
    """Lấy giỏ hàng của user (admin only)"""
    cart = CartService.get_by_user_id(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/session/{session_id}", response_model=CartModel)
def get_cart_by_session(session_id: uuid.UUID):
    """Lấy giỏ hàng theo session (khách vãng lai)"""
    cart = CartService.get_by_session_id(session_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/user/me/or-create", response_model=CartModel)
def get_or_create_my_cart(current_user_id: str = Depends(get_current_user)):
    """
    Lấy hoặc tạo giỏ hàng cho user hiện tại (từ token)
    
    **Yêu cầu:** Bearer Token trong header Authorization
    """
    return CartService.get_or_create_by_user(uuid.UUID(current_user_id))


@router.get("/user/{user_id}/or-create", response_model=CartModel)
def get_or_create_cart_by_user(user_id: uuid.UUID):
    """Lấy hoặc tạo giỏ hàng cho user"""
    return CartService.get_or_create_by_user(user_id)


@router.get("/session/{session_id}/or-create", response_model=CartModel)
def get_or_create_cart_by_session(session_id: uuid.UUID):
    """Lấy hoặc tạo giỏ hàng cho session"""
    return CartService.get_or_create_by_session(session_id)


@router.get("/{cart_id}", response_model=CartModel)
def get_cart(cart_id: uuid.UUID):
    """Lấy cart theo ID"""
    cart = CartService.get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.put("/update/{cart_id}", response_model=CartModel)
def update_cart(cart_id: uuid.UUID, cart: CartUpdateModel):
    """Cập nhật cart"""
    updated_cart = CartService.update(cart_id, cart)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return updated_cart


@router.delete("/{cart_id}")
def delete_cart(cart_id: uuid.UUID):
    """Xóa cart"""
    success = CartService.delete(cart_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {"message": "Cart deleted successfully"}


@router.get("/all", response_model=List[CartModel])
def get_all_carts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: str = Depends(get_current_admin)
):
    """Lấy danh sách tất cả carts - Chỉ admin"""
    return CartService.get_all(skip, limit)

import uuid
from typing import List
from datetime import date
from fastapi import APIRouter, Query, Body, HTTPException
from pydantic import BaseModel, Field
from models.cart_items import CartItemModel, CartItemCreateModel, CartItemUpdateModel
from services.cart_items import CartItemService

router = APIRouter(prefix="/cart-items", tags=["Cart Items"])


class AddToCartRequest(BaseModel):
    """Request body để thêm tour vào giỏ"""
    cart_id: uuid.UUID
    tour_id: uuid.UUID
    travel_date: date
    quantity: int = Field(default=1, ge=1, description="Số lượng")


@router.post("/add-to-cart", response_model=CartItemModel)
def add_to_cart(request: AddToCartRequest):
    """
    Thêm tour vào giỏ hàng - Tự động tính giá
    
    **Tự động xử lý:**
    - Kiểm tra tour có tồn tại
    - Tính giá dựa vào price_type của tour
    - Nếu item đã tồn tại thì cộng dồn số lượng
    - Lưu price_snapshot (giá tại thời điểm thêm)
    
    **Request:**
    ```json
    {
      "cart_id": "cart-uuid",
      "tour_id": "tour-uuid",
      "travel_date": "2025-12-20",
      "quantity": 2
    }
    ```
    """
    try:
        return CartItemService.add_to_cart(
            cart_id=request.cart_id,
            tour_id=request.tour_id,
            travel_date=request.travel_date,
            quantity=request.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create", response_model=CartItemModel)
def create_cart_item(item: CartItemCreateModel):
    """Tạo cart item mới (thủ công - cần tự tính giá)"""
    return CartItemService.create(item)


@router.get("/cart/{cart_id}", response_model=List[CartItemModel])
def get_cart_items(cart_id: uuid.UUID):
    """Lấy tất cả items trong giỏ hàng"""
    return CartItemService.get_by_cart_id(cart_id)


@router.get("/cart/{cart_id}/total")
def get_cart_total(cart_id: uuid.UUID):
    """Tính tổng giá trị giỏ hàng"""
    total = CartItemService.get_cart_total(cart_id)
    count = CartItemService.get_cart_count(cart_id)
    return {
        "cart_id": cart_id,
        "total_price": total,
        "total_items": count
    }


@router.get("/{cart_item_id}", response_model=CartItemModel)
def get_cart_item(cart_item_id: uuid.UUID):
    """Lấy cart item theo ID"""
    item = CartItemService.get(cart_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


@router.put("/update/{cart_item_id}", response_model=CartItemModel)
def update_cart_item(cart_item_id: uuid.UUID, item: CartItemUpdateModel):
    """Cập nhật cart item"""
    updated_item = CartItemService.update(cart_item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item


@router.patch("/update-quantity/{cart_item_id}", response_model=CartItemModel)
def update_quantity(
    cart_item_id: uuid.UUID,
    quantity: int = Query(..., ge=1, description="Số lượng mới")
):
    """Cập nhật số lượng cart item"""
    updated_item = CartItemService.update_quantity(cart_item_id, quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item


@router.delete("/{cart_item_id}")
def delete_cart_item(cart_item_id: uuid.UUID):
    """Xóa item khỏi giỏ hàng"""
    success = CartItemService.delete(cart_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart item deleted successfully"}


@router.delete("/cart/{cart_id}/clear")
def clear_cart(cart_id: uuid.UUID):
    """Xóa tất cả items trong giỏ hàng"""
    CartItemService.clear_cart(cart_id)
    return {"message": "Cart cleared successfully"}

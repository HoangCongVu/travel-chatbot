from fastapi import APIRouter, HTTPException, Query
import uuid
from models.user import UserCreateModel, UserUpdateModel, UserModel
from services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserModel)
def create_user(user: UserCreateModel):
    return UserService.create_user(user)


@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: uuid.UUID):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserModel)
def update_user(user_id: uuid.UUID, user: UserUpdateModel):
    updated = UserService.update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: uuid.UUID):
    deleted = UserService.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.get("/", response_model=list[UserModel])
def list_users(
    limit: int = Query(100, ge=1, le=500, description="Số user tối đa trả về"),
    offset: int = Query(0, ge=0, description="Bỏ qua số user đầu")
):
    return UserService.get_all_users(limit=limit, offset=offset)

import uuid
from fastapi import APIRouter
from models.user import UserCreateModel, UserModel, UserLoginModel, UserLoginResponse
from services.user import UserService 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login", response_model=UserLoginResponse)
def login_user(login_data: UserLoginModel):
    return UserService.login(login_data)

@router.post("/create", response_model=UserModel)
def create_user(user: UserCreateModel):
    return UserService.create_user(user)

@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: uuid.UUID):
    return UserService.get_user(user_id)

@router.put("/{user_id}", response_model=UserModel)
def update_user(user_id: uuid.UUID, user: UserCreateModel):
    return UserService.update_user(user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID):
    return UserService.delete_user(user_id)

@router.get("/", response_model=list[UserModel])
def get_all_user():
    return UserService.get_all_user()


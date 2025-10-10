import uuid
from models.user import UserCreateModel, UserModel, UserLoginModel, UserLoginResponse
from fastapi import HTTPException
from repositories.user import UserRespository

class UserService():
    @staticmethod
    def create_user(payload: UserCreateModel):
        return UserRespository.create(payload)
    
    @staticmethod
    def get_user(payload: uuid.UUID):
        return UserRespository.get(payload)
    
    @staticmethod
    def update_user(id: uuid.UUID, data: UserCreateModel):
        return UserRespository.update(id = id, data = data)
    
    @staticmethod
    def delete_user(payload: uuid.UUID):
        return UserRespository.delete(payload)
    
    @staticmethod
    def get_all_user():
        return UserRespository.get_all_user()
    
    @staticmethod
    def get_by_email(payload: UserCreateModel) -> UserModel:
        # Kiểm tra email đã tồn tại
        existing_user = UserRespository.get_by_email(payload.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Tạo user mới
        return UserRespository.create(payload)
    
    @staticmethod
    def login(email: str, password: str) -> UserLoginResponse:
        # Kiểm tra thông tin đăng nhập
        user = UserRespository.login(email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Bỏ các kiểm tra thuộc tính không tồn tại
        return UserLoginResponse(user=user, message="Login successful")
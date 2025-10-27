import uuid
from models.user import UserCreateModel, UserModel, UserLoginModel, UserLoginResponse
from fastapi import HTTPException
from repositories.user import UserRespository
import jwt
import datetime
from middleware.auth import SECRET_KEY, ALGORITHM

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
        return None
    
    @staticmethod
    def login(login_data: UserLoginModel) -> UserLoginResponse:
        user = UserRespository.login(login_data.email, login_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        payload = {
            "sub": str(user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return UserLoginResponse(
            access_token=token,
            token_type="bearer"
        )

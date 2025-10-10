import uuid
from models.user import UserCreateModel, UserTable, UserModel, UserLoginModel, UserLoginResponse
from db import Session
from utils.pkdf2 import hash_password_pbkdf2, verify_password

class UserRespository():
    @staticmethod
    def create(payload: UserCreateModel) -> UserModel:
        with Session() as session:
            hashed_password, salt = hash_password_pbkdf2(payload.password)
            
            user_data = payload.model_dump()
            # Lưu hash và salt cách nhau bằng dấu ':'
            user_data['password'] = f"{hashed_password}:{salt}"
            
            user = UserTable(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return UserModel.model_validate(user)

    @staticmethod
    def get(payload: uuid.UUID) -> UserModel:
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.id == payload).first()
            if user:
                return UserModel.model_validate(user)
            return UserModel(id=payload, first_name='sample', last_name='sample', email='sample', phone_number='sample', password='sample', role_id=1, is_active=True, is_verified=True, is_deleted=False)
        
    @staticmethod
    def update(id: uuid.UUID, data: UserCreateModel):
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.id == id).first()
            if not user:
                return None
            for key, value in data.model_dump().items():
                setattr(user, key, value)
            session.commit()
            session.refresh(user)
            return UserModel.model_validate(user)
        
    @staticmethod
    def delete(payload: uuid.UUID):
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.id == payload).first()
            if user:
                session.delete(user)
                session.commit()
            return user
        
    @staticmethod
    def get_all_user():
        with Session() as session:
            users = session.query(UserTable).all()
            return [UserModel.model_validate(user) for user in users]    

    @staticmethod
    def get_by_email(email: str) -> UserModel:
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.email == email).first()
            if user:
                return UserModel.model_validate(user)
            return None
    
    @staticmethod
    def login(email: str, password: str) -> UserModel:
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.email == email).first()
            if not user:
                return None
            
            # Tách hash và salt từ password đã lưu
            stored_password = user.password
            if ':' not in stored_password:
                return None  # Invalid password format
            
            stored_hash, stored_salt = stored_password.split(':', 1)
            
            # Verify password
            if verify_password(stored_hash, stored_salt, password):
                return UserModel.model_validate(user)
            
            return None
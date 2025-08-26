import uuid
from models.user import UserCreateModel
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
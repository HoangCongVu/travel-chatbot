import uuid
from typing import Optional
from models.user import UserCreateModel, UserUpdateModel, UserModel
from repositories.user import UserRepository


class UserService:
    @staticmethod
    def create_user(payload: UserCreateModel) -> UserModel:
        return UserRepository.create(payload)

    @staticmethod
    def get_user(user_id: uuid.UUID) -> Optional[UserModel]:
        return UserRepository.get(user_id)

    @staticmethod
    def update_user(user_id: uuid.UUID, data: UserUpdateModel) -> Optional[UserModel]:
        return UserRepository.update(user_id=user_id, data=data)

    @staticmethod
    def delete_user(user_id: uuid.UUID) -> bool:
        return UserRepository.delete(user_id)

    @staticmethod
    def get_all_users(limit: int = 100, offset: int = 0) -> list[UserModel]:
        return UserRepository.get_all(limit=limit, offset=offset)

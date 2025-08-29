import uuid
from typing import Optional
from models.user import UserCreateModel, UserUpdateModel, UserTable, UserModel
from db import Session


class UserRepository:
    @staticmethod
    def create(payload: UserCreateModel) -> UserModel:
        with Session() as session:
            user = UserTable(**payload.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            return UserModel.model_validate(user)

    @staticmethod
    def get(user_id: uuid.UUID) -> Optional[UserModel]:
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.id == user_id).first()
            return UserModel.model_validate(user) if user else None

    @staticmethod
    def update(user_id: uuid.UUID, data: UserUpdateModel) -> Optional[UserModel]:
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.id == user_id).first()
            if not user:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            session.commit()
            session.refresh(user)
            return UserModel.model_validate(user)

    @staticmethod
    def delete(user_id: uuid.UUID) -> bool:
        with Session() as session:
            user = session.query(UserTable).filter(UserTable.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False

    @staticmethod
    def get_all(limit: int = 100, offset: int = 0) -> list[UserModel]:
        with Session() as session:
            users = session.query(UserTable).offset(offset).limit(limit).all()
            return [UserModel.model_validate(user) for user in users]

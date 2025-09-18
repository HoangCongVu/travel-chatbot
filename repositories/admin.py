import uuid
from db import Session
from models.admin import Admin, CreateAdminModel, UpdateAdminModel, AdminModel


class AdminRepositories:
    @staticmethod
    def create(payload: CreateAdminModel) -> AdminModel:
        with Session() as session:
            admin = Admin(**payload.model_dump())
            session.add(admin)
            session.commit()
            session.refresh(admin)
            return AdminModel.model_validate(admin, from_attributes=True)

    @staticmethod
    def get_all() -> list[AdminModel]:
        with Session() as session:
            admins = session.query(Admin).all()
            return [AdminModel.model_validate(a, from_attributes=True) for a in admins]

    @staticmethod
    def get_one(admin_id: uuid.UUID) -> AdminModel | None:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.id == admin_id).first()
            if admin:
                return AdminModel.model_validate(admin, from_attributes=True)
            return None

    @staticmethod
    def update(admin_id: uuid.UUID, payload: UpdateAdminModel) -> AdminModel | None:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.id == admin_id).first()
            if admin:
                update_data = payload.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(admin, key, value)
                session.commit()
                session.refresh(admin)
                return AdminModel.model_validate(admin, from_attributes=True)
            return None

    @staticmethod
    def delete(admin_id: uuid.UUID) -> bool:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.id == admin_id).first()
            if admin:
                session.delete(admin)
                session.commit()
                return True
            return False

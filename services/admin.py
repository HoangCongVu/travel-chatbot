import uuid
from repositories.admin import AdminRepositories
from models.admin import CreateAdminModel, UpdateAdminModel, AdminModel


class AdminService:
    @staticmethod
    def create(payload: CreateAdminModel) -> AdminModel:
        return AdminRepositories.create(payload)

    @staticmethod
    def get_all() -> list[AdminModel]:
        return AdminRepositories.get_all()

    @staticmethod
    def get(admin_id: uuid.UUID) -> AdminModel | None:
        return AdminRepositories.get_one(admin_id)

    @staticmethod
    def update(admin_id: uuid.UUID, payload: UpdateAdminModel) -> AdminModel | None:
        return AdminRepositories.update(admin_id, payload)

    @staticmethod
    def delete(admin_id: uuid.UUID) -> bool:
        return AdminRepositories.delete(admin_id)

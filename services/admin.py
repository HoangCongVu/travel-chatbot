import uuid
from repositories.admin import AdminRepositories
from models.admin import CreateAdminModel, UpdateAdminModel, AdminModel, AdminLoginModel, AdminLoginResponse
from fastapi import HTTPException


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

    @staticmethod
    def get_by_email(payload: AdminLoginModel) -> AdminModel:
        # Kiểm tra email đã tồn tại
        existing_admin = AdminRepositories.get_by_email(payload.email)
        if existing_admin:
            raise HTTPException(status_code=400, detail="Email already registered")
        return admin

    @staticmethod
    def login(email: str, password: str) -> AdminLoginResponse:
        # Kiểm tra thông tin đăng nhập
        admin = AdminRepositories.login(email, password)
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Bỏ các kiểm tra thuộc tính không tồn tại
        return AdminLoginResponse(admin=admin, message="Login successful")
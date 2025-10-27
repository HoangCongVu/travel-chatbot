import uuid
from repositories.admin import AdminRepositories
from models.admin import CreateAdminModel, UpdateAdminModel, AdminModel, AdminLoginModel, AdminLoginResponse
from fastapi import HTTPException
import jwt
import datetime
from middleware.auth import SECRET_KEY, ALGORITHM


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
        return None

    def login(login_data: AdminLoginModel) -> AdminLoginResponse:
        admin = AdminRepositories.login(login_data.email, login_data.password)
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        payload = {
            "sub": str(admin.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return AdminLoginResponse(
            access_token=token,
            token_type="bearer"
        )
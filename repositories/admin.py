import uuid
from db import Session
from models.admin import Admin, CreateAdminModel, UpdateAdminModel, AdminModel, AdminLoginModel, AdminLoginResponse
from utils.pkdf2 import hash_password_pbkdf2, verify_password


class AdminRepositories:
    @staticmethod
    def create(payload: CreateAdminModel) -> AdminModel:
        with Session() as session:
            hashed_password, salt = hash_password_pbkdf2(payload.password)
            
            admin_data = payload.model_dump()
            # Lưu hash và salt cách nhau bằng dấu ':'
            admin_data['password'] = f"{hashed_password}:{salt}"
            admin = Admin(**admin_data)
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

    @staticmethod
    def get_by_email(email: str) -> AdminModel:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.email == email).first()
            if admin:
                return AdminModel.model_validate(admin, from_attributes=True)
            return None
    
    @staticmethod
    def get_staff_admins() -> list[AdminModel]:
        with Session() as session:
            staff_admins = session.query(Admin).filter(Admin.role == "staff").all()
            return [AdminModel.model_validate(admin, from_attributes=True) for admin in staff_admins]
    
    @staticmethod
    def login(email: str, password: str) -> AdminModel:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.email == email).first()
            if not admin:
                return None
            
            # Tách hash và salt từ password đã lưu
            stored_password = admin.password
            if ':' not in stored_password:
                return None  # Invalid password format
            
            stored_hash, stored_salt = stored_password.split(':', 1)
            
            # Verify password
            if verify_password(stored_hash, stored_salt, password):
                return AdminModel.model_validate(admin, from_attributes=True)
            
            return None
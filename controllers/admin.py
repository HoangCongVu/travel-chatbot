import uuid
from fastapi import APIRouter, HTTPException
from models.admin import CreateAdminModel, UpdateAdminModel, AdminModel
from services.admin import AdminService

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("", response_model=AdminModel)
def create_admin(payload: CreateAdminModel):
    return AdminService.create(payload)


@router.get("", response_model=list[AdminModel])
def get_all_admins():
    return AdminService.get_all()


@router.get("/{admin_id}", response_model=AdminModel)
def get_admin_by_id(admin_id: uuid.UUID):
    admin = AdminService.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


@router.put("/{admin_id}", response_model=AdminModel)
def update_admin(admin_id: uuid.UUID, payload: UpdateAdminModel):
    updated_admin = AdminService.update(admin_id, payload)
    if not updated_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return updated_admin


@router.delete("/{admin_id}")
def delete_admin(admin_id: uuid.UUID):
    success = AdminService.delete(admin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin deleted successfully"}

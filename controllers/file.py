import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from services.file import FileService
from models.file import FileCreateModel, FileModel, UploadResultModel


router = APIRouter(prefix="/files", tags=["Files"])

# Tạo file thủ công (nếu không dùng upload)
@router.post("/", response_model=FileModel)
def create_file(payload: FileCreateModel):
    return FileService.create_file(payload)


# Lấy toàn bộ file
@router.get("/", response_model=list[FileModel])
def get_all_files():
    return FileService.get_all_files()


# Lấy 1 file theo ID
@router.get("/{file_id}", response_model=FileModel)
def get_file(file_id: uuid.UUID):
    return FileService.get_file(file_id)


# Cập nhật file
@router.put("/{file_id}", response_model=FileModel)
def update_file(file_id: uuid.UUID, payload: FileCreateModel):
    return FileService.update_file(file_id, payload)


# Xóa file
@router.delete("/{file_id}")
def delete_file(file_id: uuid.UUID):
    FileService.delete_file(file_id)
    return {"message": "File deleted successfully"}

import uuid
import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from models.file import UploadResultModel
from services.file import FileService
from utils.file_reader import readFileFromUrl

router = APIRouter(prefix="/upload-files", tags=["Files"])

# Upload + lưu DB + đọc nội dung file luôn
@router.post("/upload", response_model=dict)
async def upload_and_read_file(
    admin_id: uuid.UUID,
    file: UploadFile = File(...)
):
    try:
        # Upload & lưu DB
        file_bytes = await file.read()
        upload_result: UploadResultModel = FileService.upload_and_create_file(
            file_bytes, file.filename, admin_id
        )

        # Đọc nội dung file từ URL đã upload
        content = readFileFromUrl(upload_result.url)

        return {
            "message": "Upload & read file successfully",
            "url": upload_result.url,
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

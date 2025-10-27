import uuid
import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from models.file import UploadResultModel
from models.admin import AdminModel
from services.file import FileService
from services.admin import AdminService
from utils.file_reader import readFileFromUrl
from middleware.auth import get_current_admin


router = APIRouter(prefix="/upload-files", tags=["Files"])

@router.post("/uploadImage", response_model=dict)
async def upload_file_only(
    file: UploadFile = File(...),
    current_admin: str = Depends(get_current_admin)
):
    try:
        file_bytes = await file.read()

        upload_result = FileService.upload_and_create_file(
            file_bytes=file_bytes,
            file_name=file.filename,
            admin_id=current_admin, 
        )

        return {
            "message": "File uploaded successfully",
            "url": upload_result.url,
            # "uploaded_by": None,
            # "admin_id": current_admin
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

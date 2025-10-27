import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from models.file import UploadResultModel
from services.file import FileService
from services.admin import AdminService
from services.agent_tour import AgentTourService
from utils.file_reader import readFileFromUrl
from middleware.auth import get_current_admin

router = APIRouter(prefix="/upload-files-agent", tags=["Files"])

@router.post("/upload", response_model=dict)
async def upload_and_process_file(
    file: UploadFile = File(...),
    current_admin: str = Depends(get_current_admin)
):
    try:
        file_bytes = await file.read()
        upload_result: UploadResultModel = FileService.upload_and_create_file(
            file_bytes, file.filename, current_admin  # Truyền admin object
        )

        # 3. Đọc nội dung file
        content = readFileFromUrl(upload_result.url)
        if not content.strip():
            raise HTTPException(status_code=400, detail="File is empty or unsupported format")

        # 4. Dùng AgentTourService để phân tích nội dung
        tour_data = AgentTourService.extract_info_from_text(content)

        return {
            "message": "Upload, read & process file successfully",
            "file_url": upload_result.url,
            "tour_data": tour_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

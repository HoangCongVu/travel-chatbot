import cloudinary
import cloudinary.uploader
from models.file import UploadResultModel
import os
from fastapi import HTTPException


cloudinary.config(
    cloud_name="dq1mvlfoo",
    api_key="564782668566336",
    api_secret="yBH9RIDrLnnPfFfGsohOWdJSt6w"
)

def upload_file_to_cloudinary(file_bytes: bytes, file_name: str) -> str:
    ext = os.path.splitext(file_name)[1].lower()

    # PDF hoặc các loại không phải ảnh → dùng resource_type="raw"
    resource_type = "raw" if ext in [".pdf", ".docx", ".txt"] else "auto"

    result = cloudinary.uploader.upload(
        file_bytes,
        resource_type=resource_type,
        public_id=file_name,
        access_mode="public"
    )
    return result.get("secure_url")
    
def handle_upload_file(file_bytes: bytes, file_name: str) -> UploadResultModel:
    url = upload_file_to_cloudinary(file_bytes, file_name)
    if not url:
        raise HTTPException(status_code=500, detail="Không thể upload file lên Cloudinary")
    return UploadResultModel(message="Upload lên cloud và lưu thành công", url=url)

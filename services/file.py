import uuid
from fastapi import HTTPException
from models.file import UploadResultModel, FileCreateModel, FileModel
from repositories.file import FileRepositories
from utils.cloudinary import handle_upload_file


class FileService:
    @staticmethod
    def upload_and_create_file(file_bytes: bytes, file_name: str, admin_id: uuid.UUID) -> UploadResultModel:
        # Upload lên Cloudinary
        upload_result = handle_upload_file(file_bytes, file_name)

        # Tạo bản ghi trong DB
        new_file = FileCreateModel(
            admin_id=admin_id,
            file_name=file_name,
            file_url=upload_result.url,
        )
        FileRepositories.create(new_file)

        return upload_result

    @staticmethod
    def create_file(new_file: FileCreateModel) -> FileModel:
        return FileRepositories.create(new_file)

    @staticmethod
    def get_all_files() -> list[FileModel]:
        return FileRepositories.get_all()

    @staticmethod
    def get_file(file_id: uuid.UUID) -> FileModel:
        file = FileRepositories.get_one(file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        return file

    @staticmethod
    def update_file(file_id: uuid.UUID, payload: FileCreateModel) -> FileModel:
        file = FileRepositories.update(file_id, payload)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        return file

    @staticmethod
    def delete_file(file_id: uuid.UUID) -> bool:
        deleted = FileRepositories.delete(file_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="File not found")
        return True

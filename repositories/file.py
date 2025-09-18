import uuid
from db import Session
from models.file import FileCreateModel, FileModel, FileTable


class FileRepositories:
    @staticmethod
    def create(payload: FileCreateModel) -> FileModel:
        with Session() as session:
            file = FileTable(**payload.model_dump())
            session.add(file)
            session.commit()
            session.refresh(file)
            return FileModel.model_validate(file, from_attributes=True)

    @staticmethod
    def get_all() -> list[FileModel]:
        with Session() as session:
            files = session.query(FileTable).all()
            return [FileModel.model_validate(file, from_attributes=True) for file in files]

    @staticmethod
    def get_one(file_id: uuid.UUID) -> FileModel | None:
        with Session() as session:
            file = session.query(FileTable).filter(FileTable.id == file_id).first()
            if file:
                return FileModel.model_validate(file, from_attributes=True)
            return None

    @staticmethod
    def update(file_id: uuid.UUID, updated_file: FileCreateModel) -> FileModel | None:
        with Session() as session:
            file = session.query(FileTable).filter(FileTable.id == file_id).first()
            if file:
                file.file_name = updated_file.file_name
                file.file_url = updated_file.file_url
                session.commit()
                session.refresh(file)
                return FileModel.model_validate(file, from_attributes=True)
            return None

    @staticmethod
    def delete(file_id: uuid.UUID) -> bool:
        with Session() as session:
            file = session.query(FileTable).filter(FileTable.id == file_id).first()
            if file:
                session.delete(file)
                session.commit()
                return True
            return False

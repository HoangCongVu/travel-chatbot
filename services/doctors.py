import uuid
from models.doctors import (
    CreateDoctorPayload,
    UpdateDoctorPayload,
    DoctorModel
)
from repositories.doctors import DoctorRepository


class DoctorService:
    @staticmethod
    def create(payload: CreateDoctorPayload) -> DoctorModel:
        return DoctorRepository.create(payload)

    @staticmethod
    def get(doctor_id: uuid.UUID) -> DoctorModel | None:
        return DoctorRepository.get_one(doctor_id)

    @staticmethod
    def get_all() -> list[DoctorModel]:
        return DoctorRepository.get_all()

    @staticmethod
    def update(doctor_id: uuid.UUID, payload: UpdateDoctorPayload) -> DoctorModel | None:
        return DoctorRepository.update(doctor_id, payload)

    @staticmethod
    def delete(doctor_id: uuid.UUID) -> bool:
        return DoctorRepository.delete(doctor_id)

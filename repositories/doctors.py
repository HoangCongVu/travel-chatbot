import uuid
from datetime import timezone
from db import Session
from models.doctors import DoctorTable, CreateDoctorPayload, UpdateDoctorPayload, DoctorModel


class DoctorRepository:
    @staticmethod
    def create(payload: CreateDoctorPayload) -> DoctorModel:
        with Session() as session:
            doctor = DoctorTable(**payload.model_dump())
            session.add(doctor)
            session.commit()
            session.refresh(doctor)
            return DoctorModel.model_validate(doctor, from_attributes=True)

    @staticmethod
    def get_one(doctor_id: uuid.UUID) -> DoctorModel | None:
        with Session() as session:
            doctor = session.get(DoctorTable, doctor_id)
            if not doctor:
                return None
            return DoctorModel.model_validate(doctor, from_attributes=True)

    @staticmethod
    def get_all() -> list[DoctorModel]:
        with Session() as session:
            doctors = session.query(DoctorTable).all()
            return [DoctorModel.model_validate(doc, from_attributes=True) for doc in doctors]

    @staticmethod
    def update(doctor_id: uuid.UUID, payload: UpdateDoctorPayload) -> DoctorModel | None:
        with Session() as session:
            doctor = session.get(DoctorTable, doctor_id)
            if not doctor:
                return None

            for field, value in payload.model_dump(exclude_unset=True).items():
                setattr(doctor, field, value)

            session.commit()
            session.refresh(doctor)
            return DoctorModel.model_validate(doctor, from_attributes=True)

    @staticmethod
    def delete(doctor_id: uuid.UUID) -> bool:
        with Session() as session:
            doctor = session.get(DoctorTable, doctor_id)
            if not doctor:
                return False
            session.delete(doctor)
            session.commit()
            return True

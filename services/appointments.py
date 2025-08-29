import uuid

from models.appointments import Appointments, CreateAppointments, UpdateAppointments,AppointmentsModel
from db import Session

from repositories.appointments import AppointmentsRepository

class AppointmentService:
    @staticmethod
    def create_appointment(payload: CreateAppointments) -> AppointmentsModel:
        return AppointmentsRepository.create(payload)
    
    @staticmethod
    def get_appointment(appointment_id: str) -> AppointmentsModel | None:
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return None
        return AppointmentsRepository.get_by_id(appointment_uuid)
    
    @staticmethod
    def get_all_appointments() -> list[AppointmentsModel]:
        return AppointmentsRepository.get_all()
    
    @staticmethod
    def update_appointment(appointment_id: str, payload: UpdateAppointments) -> AppointmentsModel | None:
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return None
        return AppointmentsRepository.update(appointment_uuid, payload)
    
    @staticmethod
    def delete_appointment(appointment_id: str) -> bool:
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return False
        return AppointmentsRepository.delete(appointment_uuid)
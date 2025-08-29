import uuid

from models.appointments import Appointments, CreateAppointments, UpdateAppointments,AppointmentsModel
from db import Session

class AppointmentsRepository:
    @staticmethod
    def create(payload: CreateAppointments) -> AppointmentsModel:
        with Session() as session:
            appointment = Appointments(**payload.model_dump())
            session.add(appointment)
            session.commit()
            session.refresh(appointment)
            return AppointmentsModel.model_validate(appointment,from_attributes=True)
        
    @staticmethod
    def get_by_id(appointment_id: uuid.UUID) -> AppointmentsModel | None:
        with Session() as session:
            appointment = session.get(Appointments, appointment_id)
            if appointment:
                return AppointmentsModel.model_validate(appointment,from_attributes=True)
            return None
        
    @staticmethod
    def get_all() -> list[AppointmentsModel]:
        with Session() as session:
            appointments = session.query(Appointments).all()
            return [AppointmentsModel.model_validate(app,from_attributes=True) for app in appointments]

    @staticmethod
    def update(appointment_id: uuid.UUID, payload: UpdateAppointments) -> AppointmentsModel | None:
        with Session() as session:
            appointment = session.get(Appointments, appointment_id)
            if not appointment:
                return None
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(appointment, key, value)
            session.commit()
            session.refresh(appointment)
            return AppointmentsModel.model_validate(appointment,from_attributes=True)
    
    @staticmethod
    def delete(appointment_id: uuid.UUID) -> bool:
        with Session() as session:
            appointment = session.get(Appointments, appointment_id)
            if not appointment:
                return False
            session.delete(appointment)
            session.commit()
            return True
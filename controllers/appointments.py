import uuid
from fastapi import APIRouter, HTTPException, status
from services.appointments import AppointmentService
from models.appointments import CreateAppointments, UpdateAppointments, AppointmentsModel

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("", response_model=AppointmentsModel, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: CreateAppointments):
    return AppointmentService.create_appointment(appointment)

@router.get("/", response_model=list[AppointmentsModel])
def get_appointments():
    return AppointmentService.get_all_appointments()

@router.get("/{appointment_id}", response_model=AppointmentsModel)
def get_appointment(appointment_id: str):
    appointment = AppointmentService.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentsModel)
def update_appointment(appointment_id: str, appointment: UpdateAppointments):
    updated_appointment = AppointmentService.update_appointment(appointment_id, appointment)
    if not updated_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return updated_appointment

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: str):
    success = AppointmentService.delete_appointment(appointment_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}
import uuid
from fastapi import APIRouter, HTTPException
from models.doctors import (
    CreateDoctorPayload,
    UpdateDoctorPayload,
    DoctorModel
)
from services.doctors import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("", response_model=DoctorModel)
def create_doctor(payload: CreateDoctorPayload):
    return DoctorService.create(payload)


@router.get("/{doctor_id}", response_model=DoctorModel)
def get_doctor(doctor_id: uuid.UUID):
    doctor = DoctorService.get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.get("/all", response_model=list[DoctorModel])
def get_all_doctors():
    return DoctorService.get_all()


@router.put("/{doctor_id}", response_model=DoctorModel)
def update_doctor(doctor_id: uuid.UUID, payload: UpdateDoctorPayload):
    doctor = DoctorService.update(doctor_id, payload)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: uuid.UUID):
    success = DoctorService.delete(doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}

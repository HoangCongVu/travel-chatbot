import uuid
from fastapi import APIRouter, HTTPException
from models.departure_schedule import (
    CreateDepartureSchedule,
    UpdateDepartureSchedule,
    DepartureScheduleModel
)
from services.departure_schedule import DepartureScheduleService

router = APIRouter(prefix="/departure-schedules", tags=["Departure Schedules"])


@router.post("", response_model=DepartureScheduleModel)
def create_departure_schedule(payload: CreateDepartureSchedule):
    return DepartureScheduleService.create(payload)


@router.get("", response_model=DepartureScheduleModel)
def get_departure_schedule(schedule_id: uuid.UUID):
    return DepartureScheduleService.get(schedule_id)


@router.put("", response_model=DepartureScheduleModel)
def update_departure_schedule(schedule_id: uuid.UUID, payload: UpdateDepartureSchedule):
    return DepartureScheduleService.update(schedule_id, payload)


@router.delete("")
def delete_departure_schedule(schedule_id: uuid.UUID):
    DepartureScheduleService.delete(schedule_id)
    return {"message": "Departure schedule deleted successfully"}
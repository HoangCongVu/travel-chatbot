import uuid
from fastapi import APIRouter
from models.recurring_schedule import (
    CreateRecurringSchedulePayload,
    UpdateRecurringSchedulePayload,
    RecurringScheduleModel
)
from services.recurring_schedule import RecurringScheduleService


router = APIRouter(prefix="/recurring-schedules", tags=["Recurring Schedules"])

@router.post("", response_model=RecurringScheduleModel)
def create_schedule(payload: CreateRecurringSchedulePayload):
    return RecurringScheduleService.create(payload)

@router.get("", response_model=RecurringScheduleModel)
def get_schedule(schedule_id: uuid.UUID):
    return RecurringScheduleService.get(schedule_id)

@router.put("", response_model=RecurringScheduleModel)
def update_schedule(schedule_id: uuid.UUID, payload: UpdateRecurringSchedulePayload):
    return RecurringScheduleService.update(schedule_id, payload)

@router.delete("")
def delete_schedule(schedule_id: uuid.UUID):
    RecurringScheduleService.delete(schedule_id)
    return {"message": "Recurring schedule deleted successfully"}
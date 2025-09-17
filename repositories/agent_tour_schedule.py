import json
import uuid
from agents.agent_tour_schedule import agent_tour_schedule
from services.departure_schedule import DepartureScheduleService
from services.recurring_schedule import RecurringScheduleService
from services.specific_departure import SpecificDepartureService
from models.departure_schedule import CreateDepartureSchedule
from models.recurring_schedule import CreateRecurringSchedule
from models.specific_departure import CreateSpecificDeparture


class AgentTourScheduleRepository:
    @staticmethod
    def extract_schedules_from_text(payload: str, tour_id: uuid.UUID) -> dict:
        try:
            # Gọi agent đúng tên
            reply = agent_tour_schedule.generate_reply(
                messages=[{"role": "user", "content": payload}]
            )

            try:
                data = json.loads(reply)
            except json.JSONDecodeError:
                data = {"departure_schedules": []}

            results = []
            for sched in data.get("departure_schedules", []):
                schedule_type = sched.get("schedule_type")

                # Tạo departure_schedule record
                dep_schedule_record = CreateDepartureSchedule(
                    tour_id=tour_id,
                    schedule_type=schedule_type
                )
                dep_schedule = DepartureScheduleService.create(dep_schedule_record)

                if schedule_type == "recurring":
                    if not sched.get("start_date") or not sched.get("end_date"):
                        continue  # bỏ qua nếu thiếu dữ liệu bắt buộc

                    recurring_record = CreateRecurringSchedule(
                        schedule_id=dep_schedule.id,
                        recurrence_type=sched.get("recurrence_type", "custom"),
                        start_date=sched["start_date"],
                        end_date=sched["end_date"],
                        weekdays=sched.get("weekdays", [])
                    )
                    recurring = RecurringScheduleService.create(recurring_record)

                    results.append({
                        "schedule_type": "recurring",
                        "departure_schedule_id": dep_schedule.id,
                        "recurring_schedule": {
                            "id": recurring.id,
                            "recurrence_type": recurring.recurrence_type,
                            "start_date": str(recurring.start_date),
                            "end_date": str(recurring.end_date),
                            "weekdays": recurring.weekdays
                        }
                    })

                elif schedule_type == "specific":
                    specific_list = []
                    for date in sched.get("specific_dates", []):
                        specific_record = CreateSpecificDeparture(
                            schedule_id=dep_schedule.id,
                            date=date
                        )
                        specific = SpecificDepartureService.create(specific_record)
                        specific_list.append({
                            "id": specific.id,
                            "date": str(specific.date)
                        })

                    results.append({
                        "schedule_type": "specific",
                        "departure_schedule_id": dep_schedule.id,
                        "specific_departures": specific_list
                    })

            return {
                "tour_id": tour_id,
                "departure_schedules": results
            }

        except Exception as e:
            print("❌ Lỗi khi trích xuất lịch trình tour:", str(e))
            return {
                "error": "Không thể xử lý dữ liệu đầu vào",
                "message": str(e)
            }

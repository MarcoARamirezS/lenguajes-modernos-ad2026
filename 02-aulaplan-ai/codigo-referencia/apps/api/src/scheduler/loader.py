from src.repositories.base import FirestoreRepository
from src.scheduler.domain import (
    Availability, Constraint, Group, Offering, Room, SchedulerContext,
    Subject, Teacher, TimeBlock,
)


def _active(rows: list[dict]) -> list[dict]:
    return [row for row in rows if row.get("active", True)]


def load_scheduler_context(academic_period_id: str) -> SchedulerContext:
    teachers = _active(FirestoreRepository("teachers").list())
    subjects = _active(FirestoreRepository("subjects").list())
    groups = _active(FirestoreRepository("groups").list({"academic_period_id": academic_period_id}))
    rooms = _active(FirestoreRepository("rooms").list())
    blocks = _active(FirestoreRepository("time_blocks").list())
    offerings = _active(FirestoreRepository("course_offerings").list({"academic_period_id": academic_period_id}))
    availability = FirestoreRepository("teacher_availability").list()
    constraints = _active(FirestoreRepository("constraints").list())

    return SchedulerContext(
        teachers={x["id"]: Teacher(x["id"], x["name"], x["max_daily_blocks"], x["max_weekly_blocks"]) for x in teachers},
        subjects={x["id"]: Subject(x["id"], x["name"], x["weekly_blocks"], x["required_room_type"]) for x in subjects},
        groups={x["id"]: Group(x["id"], x["name"], x["student_count"]) for x in groups},
        rooms={x["id"]: Room(x["id"], x["name"], x["capacity"], x["type"]) for x in rooms},
        time_blocks={x["id"]: TimeBlock(x["id"], x["day"], x["start_time"], x["end_time"], x["order"]) for x in blocks},
        offerings={x["id"]: Offering(x["id"], x["subject_id"], x["group_id"], x["teacher_id"], x["academic_period_id"]) for x in offerings},
        availability=[Availability(x["teacher_id"], x["time_block_id"], x.get("available", True), x.get("preference_weight", 0)) for x in availability],
        constraints=[Constraint(x["type"], x["priority"], x["target_type"], x["target_id"], x.get("weight", 0), x.get("params", {})) for x in constraints],
    )

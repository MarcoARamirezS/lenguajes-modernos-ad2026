from datetime import datetime, timezone
from flask import g

from src.core.errors import ApiError
from src.firebase.client import get_db
from src.http.responses import to_jsonable
from src.repositories.base import FirestoreRepository
from src.scheduler.loader import load_scheduler_context
from src.scheduler.solver import solve_schedule

schedules_repository = FirestoreRepository("schedules")


def generate_schedule(academic_period_id: str, max_nodes: int) -> dict:
    context = load_scheduler_context(academic_period_id)
    result = solve_schedule(context, max_nodes=max_nodes)
    if result.status != "SOLVED":
        raise ApiError("No feasible schedule found", 409, "NO_SOLUTION")

    now = datetime.now(timezone.utc)
    user = getattr(g, "current_user", {"uid": "system"})
    entries = []
    for candidate in result.assignments:
        block = context.time_blocks[candidate.time_block_id]
        entries.append({
            "offering_id": candidate.offering_id,
            "subject_id": candidate.subject_id,
            "teacher_id": candidate.teacher_id,
            "group_id": candidate.group_id,
            "room_id": candidate.room_id,
            "time_block_id": candidate.time_block_id,
            "day": block.day,
            "start_time": block.start_time,
            "end_time": block.end_time,
        })

    summary = schedules_repository.create({
        "academic_period_id": academic_period_id,
        "status": "GENERATED",
        "score": result.score,
        "nodes_visited": result.nodes_visited,
        "current_version": 1,
        "created_by": user["uid"],
    })

    version_ref = get_db().collection("schedules").document(summary["id"]).collection("versions").document("v001")
    version_ref.set({
        "version": 1,
        "score": result.score,
        "entries": entries,
        "created_at": now,
        "created_by": user["uid"],
    })

    return {**to_jsonable(summary), "entries": entries}


def list_schedules() -> list[dict]:
    return to_jsonable(schedules_repository.list())


def publish_schedule(schedule_id: str) -> dict:
    current = schedules_repository.get(schedule_id)
    if current.get("status") == "PUBLISHED":
        return to_jsonable(current)
    user = getattr(g, "current_user", {"uid": "system"})
    updated = schedules_repository.update(schedule_id, {
        "status": "PUBLISHED",
        "published_at": datetime.now(timezone.utc),
        "published_by": user["uid"],
    })
    return to_jsonable(updated)

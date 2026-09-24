from flask import Blueprint, jsonify, request

from src.auth.security import require_roles
from src.schemas.scheduling import GenerateScheduleRequest
from src.services.schedules import generate_schedule, list_schedules, publish_schedule

schedules_bp = Blueprint("schedules", __name__)


@schedules_bp.get("/schedules")
def schedules_list():
    return jsonify(list_schedules())


@schedules_bp.post("/schedules/generate")
@require_roles("ADMIN", "COORDINATOR")
def schedules_generate():
    payload = GenerateScheduleRequest.model_validate(request.get_json(silent=True) or {})
    return jsonify(generate_schedule(payload.academic_period_id, payload.max_nodes)), 201


@schedules_bp.post("/schedules/<schedule_id>/publish")
@require_roles("ADMIN", "COORDINATOR")
def schedules_publish(schedule_id: str):
    return jsonify(publish_schedule(schedule_id))

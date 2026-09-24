from flask import Blueprint, jsonify, request

from src.auth.security import require_roles
from src.http.responses import to_jsonable
from src.services.catalogs import (
    academic_periods_service, availability_service, constraints_service,
    groups_service, offerings_service, rooms_service, subjects_service,
    teachers_service, time_blocks_service,
)

catalogs_bp = Blueprint("catalogs", __name__)

SERVICES = {
    "academic-periods": academic_periods_service,
    "teachers": teachers_service,
    "subjects": subjects_service,
    "groups": groups_service,
    "rooms": rooms_service,
    "time-blocks": time_blocks_service,
    "offerings": offerings_service,
    "availability": availability_service,
    "constraints": constraints_service,
}


@catalogs_bp.get("/<resource>")
def list_records(resource: str):
    service = SERVICES.get(resource)
    if not service:
        return jsonify({"error": "NOT_FOUND"}), 404
    filters = {key: value for key, value in request.args.items()}
    return jsonify(to_jsonable(service.list(filters)))


@catalogs_bp.post("/<resource>")
@require_roles("ADMIN", "COORDINATOR")
def create_record(resource: str):
    service = SERVICES.get(resource)
    if not service:
        return jsonify({"error": "NOT_FOUND"}), 404
    row = service.create(request.get_json(silent=True) or {})
    return jsonify(to_jsonable(row)), 201


@catalogs_bp.get("/<resource>/<document_id>")
def get_record(resource: str, document_id: str):
    service = SERVICES.get(resource)
    if not service:
        return jsonify({"error": "NOT_FOUND"}), 404
    return jsonify(to_jsonable(service.get(document_id)))


@catalogs_bp.put("/<resource>/<document_id>")
@require_roles("ADMIN", "COORDINATOR")
def update_record(resource: str, document_id: str):
    service = SERVICES.get(resource)
    if not service:
        return jsonify({"error": "NOT_FOUND"}), 404
    row = service.update(document_id, request.get_json(silent=True) or {})
    return jsonify(to_jsonable(row))


@catalogs_bp.delete("/<resource>/<document_id>")
@require_roles("ADMIN", "COORDINATOR")
def delete_record(resource: str, document_id: str):
    service = SERVICES.get(resource)
    if not service:
        return jsonify({"error": "NOT_FOUND"}), 404
    service.delete(document_id)
    return "", 204

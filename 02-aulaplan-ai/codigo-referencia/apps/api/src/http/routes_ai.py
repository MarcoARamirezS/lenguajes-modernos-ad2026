from flask import Blueprint, jsonify, request

from src.ai.gemini_constraints import parse_constraints
from src.auth.security import require_roles
from src.schemas.scheduling import ParseConstraintRequest

ai_bp = Blueprint("ai", __name__)


@ai_bp.post("/ai/constraints/parse")
@require_roles("ADMIN", "COORDINATOR")
def parse_constraint_text():
    payload = ParseConstraintRequest.model_validate(request.get_json(silent=True) or {})
    result = parse_constraints(payload.text)
    return jsonify(result.model_dump())

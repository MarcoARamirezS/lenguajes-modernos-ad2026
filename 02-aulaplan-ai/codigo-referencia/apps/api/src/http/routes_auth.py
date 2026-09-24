from flask import Blueprint, g, jsonify

from src.auth.security import require_roles
from src.http.responses import to_jsonable
from src.repositories.base import FirestoreRepository

users_bp = Blueprint("users", __name__)
users_repository = FirestoreRepository("users")


@users_bp.get("/auth/me")
def me():
    return jsonify(g.current_user)


@users_bp.get("/users")
@require_roles("ADMIN")
def list_users():
    return jsonify(to_jsonable(users_repository.list()))

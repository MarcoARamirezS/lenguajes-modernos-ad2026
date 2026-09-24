from functools import wraps
from flask import g, request
from firebase_admin import auth

from src.core.errors import ApiError
from src.repositories.base import FirestoreRepository

users_repository = FirestoreRepository("users")


def authenticate_request() -> None:
    if request.method == "OPTIONS" or request.path == "/health":
        return

    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise ApiError("Authentication required", 401, "UNAUTHENTICATED")

    token = header.removeprefix("Bearer ").strip()
    try:
        decoded = auth.verify_id_token(token)
    except Exception as error:
        raise ApiError("Invalid authentication token", 401, "UNAUTHENTICATED") from error

    uid = decoded["uid"]
    try:
        profile = users_repository.get(uid)
    except ApiError as error:
        raise ApiError("User profile not found", 403, "PROFILE_NOT_FOUND") from error

    if not profile.get("active", True):
        raise ApiError("Inactive user", 403, "INACTIVE_USER")

    g.current_user = {
        "uid": uid,
        "email": decoded.get("email", ""),
        "display_name": profile.get("display_name", ""),
        "role": profile.get("role", "VIEWER"),
        "active": True,
    }


def require_roles(*roles: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if not user or user.get("role") not in roles:
                raise ApiError("Insufficient permissions", 403, "FORBIDDEN")
            return function(*args, **kwargs)
        return wrapper
    return decorator

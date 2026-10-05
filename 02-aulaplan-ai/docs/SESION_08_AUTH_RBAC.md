[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 07](./SESION_07_AVAILABILITY_CONSTRAINTS.md) · [Sesión 09 →](./SESION_09_SCHEDULER_DOMAIN_LOADER.md)

# Sesión 08 — Firebase Authentication + RBAC

**Duración:** 1 h 30 min  
**Objetivo:** validar Firebase ID tokens en Python y controlar permisos.

## Flujo

```text
Nuxt
 ↓
Firebase Auth
 ↓ ID token
Authorization: Bearer TOKEN
 ↓
Python
 ↓ verify_id_token()
users/UID
 ↓
RBAC
```

## 1. Seguridad backend

### `apps/api/src/auth/security.py`

```python
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
```


## 2. Rutas de usuario

### `apps/api/src/http/routes_auth.py`

```python
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
```


## 3. App con autenticación

```python
from flask import Flask

from src.auth.security import authenticate_request
from src.http.responses import register_error_handlers
from src.http.routes_auth import users_bp
from src.http.routes_catalogs import catalogs_bp
from src.http.routes_health import health_bp


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing
    register_error_handlers(app)

    if not testing:
        app.before_request(authenticate_request)

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(catalogs_bp)
    return app
```

## 4. Crear usuario local

En Emulator UI:

1. Authentication → Add user.
2. Crea `admin@aulaplan.local`.
3. Copia UID.
4. Firestore → `users/UID`:

```json
{
  "email": "admin@aulaplan.local",
  "display_name": "Administrador",
  "role": "ADMIN",
  "active": true
}
```

## 5. Roles

```text
ADMIN        lectura + escritura + usuarios
COORDINATOR  lectura + escritura académica
VIEWER       lectura
```

## 5.1 Bootstrap de administrador en un proyecto real

Opcionalmente puedes usar este script después de crear el usuario en Firebase Authentication.

### `apps/api/scripts/create_admin.py`

```python
import os
from firebase_admin import auth, firestore, initialize_app

initialize_app()
email = os.environ["ADMIN_EMAIL"]
user = auth.get_user_by_email(email)
firestore.client().collection("users").document(user.uid).set({
    "email": user.email,
    "display_name": user.display_name or "Administrator",
    "role": "ADMIN",
    "active": True,
})
print(f"ADMIN ready: {email} ({user.uid})")
```

Para ejecutarlo contra producción necesitas credenciales de Google válidas fuera del repositorio.

macOS/Linux:

```bash
export ADMIN_EMAIL=admin@tu-dominio.com
PYTHONPATH=. python scripts/create_admin.py
```

Windows:

```powershell
$env:ADMIN_EMAIL="admin@tu-dominio.com"
$env:PYTHONPATH="."
python scripts/create_admin.py
```

## 6. Frontend

La entrega de frontend ya obtiene `getIdToken()` y envía `Authorization: Bearer ...`.

## Checklist

- [ ] login Firebase.
- [ ] token validado.
- [ ] perfil de usuario.
- [ ] 401 sin token.
- [ ] 403 sin rol.

## Commit

```bash
git add .
git commit -m "feat: secure API with Firebase Auth and RBAC"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 07](./SESION_07_AVAILABILITY_CONSTRAINTS.md) · [Sesión 09 →](./SESION_09_SCHEDULER_DOMAIN_LOADER.md)

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 13](./SESION_13_GEMINI_AI.md) · [Sesión 15 →](./SESION_15_TESTING_CICD_DEPLOY.md)

# Sesión 14 — Generación, versionado y publicación

**Duración:** 1 h 30 min  
**Objetivo:** transformar el solver en un flujo de negocio auditable.

## Distribución

```text
00–15  estados de horario
15–35  generate service
35–55  versión inmutable
55–70  endpoints
70–82  frontend
82–90  commit
```

## 1. Estados

```text
GENERATED
PUBLISHED
```

La guía puede evolucionar posteriormente a `DRAFT`, `REVIEWED` y `ARCHIVED`.

## 2. Service

### `apps/api/src/services/schedules.py`

```python
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
```


## 3. Routes

### `apps/api/src/http/routes_schedules.py`

```python
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
```


## 4. App final

### `apps/api/src/http/app.py`

```python
from flask import Flask

from src.auth.security import authenticate_request
from src.http.responses import register_error_handlers
from src.http.routes_ai import ai_bp
from src.http.routes_auth import users_bp
from src.http.routes_catalogs import catalogs_bp
from src.http.routes_health import health_bp
from src.http.routes_schedules import schedules_bp


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing

    register_error_handlers(app)

    if not testing:
        app.before_request(authenticate_request)

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(catalogs_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(ai_bp)

    return app
```


## 5. Estructura Firestore

```text
schedules/{scheduleId}
├── academic_period_id
├── status
├── score
├── nodes_visited
├── current_version
└── versions/
    └── v001
        ├── version
        ├── score
        └── entries[]
```

Una versión generada no se sobrescribe. Cuando el modelo evolucione, crea `v002`, `v003`, etc.

## 6. Generar

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/schedules/generate   -H "Authorization: Bearer ID_TOKEN"   -H "Content-Type: application/json"   -d '{
    "academic_period_id":"PERIOD_ID",
    "max_nodes":50000
  }'
```

## 7. Publicar

```bash
curl -X POST   http://127.0.0.1:5001/PROJECT_ID/us-central1/api/schedules/SCHEDULE_ID/publish   -H "Authorization: Bearer ID_TOKEN"
```

## 8. Frontend

Las páginas `/generator` y `/schedules` entregadas al inicio ya llaman estos endpoints.

## Checklist

- [ ] contexto cargado.
- [ ] solver ejecutado.
- [ ] resultado guardado.
- [ ] versión `v001`.
- [ ] publicación protegida.
- [ ] usuario/auditoría registrada.

## Commit

```bash
git add .
git commit -m "feat: complete schedule generation and publishing workflow"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 13](./SESION_13_GEMINI_AI.md) · [Sesión 15 →](./SESION_15_TESTING_CICD_DEPLOY.md)

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 03](./SESION_03_CORE_REPOSITORY_ARCHITECTURE.md) · [Sesión 05 →](./SESION_05_SUBJECTS_GROUPS_OFFERINGS.md)

# Sesión 04 — Periodos académicos y profesores

**Duración:** 1 h 30 min  
**Objetivo:** implementar los primeros CRUD reales.

## 1. Schemas

El archivo se crea completo desde ahora:

### `apps/api/src/schemas/catalogs.py`

```python
from typing import Any, Literal
from pydantic import BaseModel, EmailStr, Field


class AcademicPeriodCreate(BaseModel):
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    start_date: str
    end_date: str
    active: bool = True


class AcademicPeriodUpdate(AcademicPeriodCreate):
    pass


class TeacherCreate(BaseModel):
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    max_daily_blocks: int = Field(default=4, ge=1, le=8)
    max_weekly_blocks: int = Field(default=16, ge=1, le=40)
    active: bool = True


class TeacherUpdate(TeacherCreate):
    pass


class SubjectCreate(BaseModel):
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    weekly_blocks: int = Field(ge=1, le=10)
    required_room_type: str = "CLASSROOM"
    active: bool = True


class SubjectUpdate(SubjectCreate):
    pass


class GroupCreate(BaseModel):
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    student_count: int = Field(ge=1, le=500)
    academic_period_id: str = Field(min_length=1)
    active: bool = True


class GroupUpdate(GroupCreate):
    pass


class RoomCreate(BaseModel):
    code: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    capacity: int = Field(ge=1, le=1000)
    type: str = "CLASSROOM"
    building: str = ""
    active: bool = True


class RoomUpdate(RoomCreate):
    pass


class TimeBlockCreate(BaseModel):
    day: Literal["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
    start_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    end_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    order: int = Field(ge=1, le=30)
    active: bool = True


class TimeBlockUpdate(TimeBlockCreate):
    pass


class OfferingCreate(BaseModel):
    academic_period_id: str = Field(min_length=1)
    subject_id: str = Field(min_length=1)
    group_id: str = Field(min_length=1)
    teacher_id: str = Field(min_length=1)
    active: bool = True


class OfferingUpdate(OfferingCreate):
    pass


class AvailabilityCreate(BaseModel):
    teacher_id: str = Field(min_length=1)
    time_block_id: str = Field(min_length=1)
    available: bool = True
    preference_weight: int = Field(default=0, ge=-100, le=100)


class AvailabilityUpdate(AvailabilityCreate):
    pass


class ConstraintCreate(BaseModel):
    type: str = Field(min_length=2, max_length=80)
    priority: Literal["HARD", "SOFT"]
    target_type: str = Field(min_length=2, max_length=40)
    target_id: str = Field(min_length=1)
    weight: int = Field(default=0, ge=-1000, le=1000)
    params: dict[str, Any] = Field(default_factory=dict)
    active: bool = True


class ConstraintUpdate(ConstraintCreate):
    pass
```


## 2. Servicios

### `apps/api/src/services/catalogs.py`

```python
from src.repositories.base import FirestoreRepository
from src.schemas.catalogs import (
    AcademicPeriodCreate, AcademicPeriodUpdate,
    AvailabilityCreate, AvailabilityUpdate,
    ConstraintCreate, ConstraintUpdate,
    GroupCreate, GroupUpdate,
    OfferingCreate, OfferingUpdate,
    RoomCreate, RoomUpdate,
    SubjectCreate, SubjectUpdate,
    TeacherCreate, TeacherUpdate,
    TimeBlockCreate, TimeBlockUpdate,
)
from src.services.crud import CrudService

academic_periods_service = CrudService(FirestoreRepository("academic_periods"), AcademicPeriodCreate, AcademicPeriodUpdate, ("code",))
teachers_service = CrudService(FirestoreRepository("teachers"), TeacherCreate, TeacherUpdate, ("code", "email"))
subjects_service = CrudService(FirestoreRepository("subjects"), SubjectCreate, SubjectUpdate, ("code",))
groups_service = CrudService(FirestoreRepository("groups"), GroupCreate, GroupUpdate, ("code",))
rooms_service = CrudService(FirestoreRepository("rooms"), RoomCreate, RoomUpdate, ("code",))
time_blocks_service = CrudService(FirestoreRepository("time_blocks"), TimeBlockCreate, TimeBlockUpdate)
offerings_service = CrudService(FirestoreRepository("course_offerings"), OfferingCreate, OfferingUpdate)
availability_service = CrudService(FirestoreRepository("teacher_availability"), AvailabilityCreate, AvailabilityUpdate)
constraints_service = CrudService(FirestoreRepository("constraints"), ConstraintCreate, ConstraintUpdate)
```


## 3. Rutas

### `apps/api/src/http/routes_catalogs.py`

```python
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
```


> Antes de la Sesión 08 todavía no existe RBAC. Para pruebas tempranas, comenta temporalmente `@require_roles(...)` y su import. En la Sesión 08 debe quedar exactamente el archivo final mostrado.

## 4. Registrar blueprint

```python
from flask import Flask
from src.http.responses import register_error_handlers
from src.http.routes_catalogs import catalogs_bp
from src.http.routes_health import health_bp

def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing
    register_error_handlers(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(catalogs_bp)
    return app
```

## 5. Probar periodo

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/academic-periods   -H "Content-Type: application/json"   -d '{"code":"2026-AD","name":"Agosto-Diciembre 2026","start_date":"2026-08-03","end_date":"2026-12-11","active":true}'
```

## 6. Probar profesor

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/teachers   -H "Content-Type: application/json"   -d '{"code":"T-001","name":"Ana Torres","email":"ana@example.com","max_daily_blocks":4,"max_weekly_blocks":16,"active":true}'
```

## Checklist

- [ ] Periodos CRUD.
- [ ] Profesores CRUD.
- [ ] 422 en payload inválido.
- [ ] 409 en código/correo duplicado.

## Commit

```bash
git add .
git commit -m "feat: implement academic periods and teachers"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 03](./SESION_03_CORE_REPOSITORY_ARCHITECTURE.md) · [Sesión 05 →](./SESION_05_SUBJECTS_GROUPS_OFFERINGS.md)

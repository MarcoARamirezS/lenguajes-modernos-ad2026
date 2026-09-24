[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 08](./SESION_08_AUTH_RBAC.md) · [Sesión 10 →](./SESION_10_CANDIDATES_HARD_CONSTRAINTS.md)

# Sesión 09 — Scheduler Domain + Loader

**Duración:** 1 h 30 min  
**Objetivo:** separar el algoritmo de Firebase y cargar un contexto inmutable.

## Regla arquitectónica

```text
Firestore
 ↓ Loader
SchedulerContext
 ↓
Algoritmos puros
```

## 1. Dominio

### `apps/api/src/scheduler/domain.py`

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Teacher:
    id: str
    name: str
    max_daily_blocks: int
    max_weekly_blocks: int


@dataclass(frozen=True)
class Subject:
    id: str
    name: str
    weekly_blocks: int
    required_room_type: str


@dataclass(frozen=True)
class Group:
    id: str
    name: str
    student_count: int


@dataclass(frozen=True)
class Room:
    id: str
    name: str
    capacity: int
    type: str


@dataclass(frozen=True)
class TimeBlock:
    id: str
    day: str
    start_time: str
    end_time: str
    order: int


@dataclass(frozen=True)
class Offering:
    id: str
    subject_id: str
    group_id: str
    teacher_id: str
    academic_period_id: str


@dataclass(frozen=True)
class Availability:
    teacher_id: str
    time_block_id: str
    available: bool
    preference_weight: int = 0


@dataclass(frozen=True)
class Constraint:
    type: str
    priority: str
    target_type: str
    target_id: str
    weight: int
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssignmentUnit:
    id: str
    offering_id: str
    sequence: int


@dataclass(frozen=True)
class Candidate:
    unit_id: str
    offering_id: str
    teacher_id: str
    group_id: str
    subject_id: str
    room_id: str
    time_block_id: str


@dataclass(frozen=True)
class ScheduledClass:
    candidate: Candidate
    score: int = 0


@dataclass
class SchedulerContext:
    teachers: dict[str, Teacher]
    subjects: dict[str, Subject]
    groups: dict[str, Group]
    rooms: dict[str, Room]
    time_blocks: dict[str, TimeBlock]
    offerings: dict[str, Offering]
    availability: list[Availability]
    constraints: list[Constraint]
```


## 2. Loader

### `apps/api/src/scheduler/loader.py`

```python
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
```


## 3. Conceptos

- `Offering`: profesor/materia/grupo.
- `Subject.weekly_blocks`: sesiones requeridas.
- `TimeBlock`: posición temporal.
- `Availability`: disponibilidad/preferencia.
- `Constraint`: reglas.
- `SchedulerContext`: snapshot completo.

## 4. Prueba manual

```python
from src.scheduler.loader import load_scheduler_context

context = load_scheduler_context("PERIOD_ID")
print("teachers", len(context.teachers))
print("offerings", len(context.offerings))
```

Ejecuta con `PYTHONPATH=.`.

## Checklist

- [ ] dataclasses puras.
- [ ] loader central.
- [ ] contexto inspeccionable.
- [ ] sin dependencia Flask en dominio.

## Commit

```bash
git add .
git commit -m "feat: create scheduler domain and firestore loader"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 08](./SESION_08_AUTH_RBAC.md) · [Sesión 10 →](./SESION_10_CANDIDATES_HARD_CONSTRAINTS.md)

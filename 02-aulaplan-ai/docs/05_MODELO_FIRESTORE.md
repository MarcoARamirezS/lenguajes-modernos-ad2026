[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Git y GitHub](./04_GIT_GITHUB_WORKFLOW.md) · [Contrato API →](./06_CONTRATO_API.md)

# 05 — Modelo Firestore

## Colecciones

```text
users
academic_periods
teachers
subjects
groups
rooms
time_blocks
teacher_availability
constraints
schedules
schedule_versions
```

## Ejemplo teacher

```json
{
  "code": "T-001",
  "name": "Profesor Demo",
  "email": "profesor@example.com",
  "active": true,
  "max_daily_blocks": 4,
  "max_weekly_blocks": 16
}
```

## Ejemplo subject

```json
{
  "code": "LM-401",
  "name": "Lenguajes Modernos",
  "weekly_blocks": 2,
  "room_type": "COMPUTER_LAB",
  "active": true
}
```

## Ejemplo constraint

```json
{
  "type": "TEACHER_UNAVAILABLE",
  "target_id": "teacher-id",
  "priority": "HARD",
  "params": {
    "day": "TUESDAY",
    "block_id": "B03"
  }
}
```

## Reglas

El cliente no debe tener permisos administrativos sobre las colecciones de negocio. Las escrituras pasan por la función Python, que valida el token y aplica RBAC.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Git y GitHub](./04_GIT_GITHUB_WORKFLOW.md) · [Contrato API →](./06_CONTRATO_API.md)

# 05 — Contrato API

Base:

```text
/api
```

## Health

```text
GET /api/health
GET /api/info
```

## Academic periods

```text
GET    /api/academic-periods
POST   /api/academic-periods
GET    /api/academic-periods/:id
PUT    /api/academic-periods/:id
DELETE /api/academic-periods/:id
```

## Teachers

```text
GET    /api/teachers
POST   /api/teachers
GET    /api/teachers/:id
PUT    /api/teachers/:id
DELETE /api/teachers/:id
```

## Subjects / Groups / Rooms / Time blocks

Se mantiene el mismo patrón REST.

## Availability

```text
GET  /api/teachers/:teacherId/availability
PUT  /api/teachers/:teacherId/availability
```

## Constraints

```text
GET    /api/constraints
POST   /api/constraints
PUT    /api/constraints/:id
DELETE /api/constraints/:id
POST   /api/ai/constraints/parse
```

## Validation

```text
POST /api/schedules/validate-input
```

Respuesta:

```json
{
  "valid": false,
  "errors": [],
  "warnings": []
}
```

## Generation

```text
POST /api/schedules/generate
```

Request:

```json
{
  "academicPeriodId": "period-1",
  "maxSolverMs": 8000,
  "seed": 42
}
```

Response:

```json
{
  "scheduleVersionId": "...",
  "status": "GENERATED",
  "score": 870,
  "hardViolations": 0,
  "softViolations": 4
}
```

## Publication

```text
GET  /api/schedules
GET  /api/schedules/:id
POST /api/schedules/:id/review
POST /api/schedules/:id/publish
POST /api/schedules/:id/archive
```

## Error envelope

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": []
  }
}
```

## Códigos

- `200` lectura/actualización correcta.
- `201` creado.
- `204` eliminado.
- `400` request inválido.
- `401` token ausente/inválido.
- `403` rol insuficiente.
- `404` recurso inexistente.
- `409` conflicto de negocio.
- `422` restricciones semánticamente inválidas.
- `500` error inesperado.

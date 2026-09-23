# AulaPlan AI — Contrato API REST

Base local:

```text
http://127.0.0.1:8000/api/v1
```

## Convenciones

- JSON UTF-8.
- IDs como `string`.
- Fechas ISO-8601.
- `Authorization: Bearer <Firebase ID Token>` en rutas privadas.
- Respuestas de error consistentes.

## Health

```text
GET /health
```

## Catálogos

```text
GET    /academic-periods
POST   /academic-periods
GET    /academic-periods/{id}
PATCH  /academic-periods/{id}
DELETE /academic-periods/{id}

GET    /teachers
POST   /teachers
GET    /teachers/{id}
PATCH  /teachers/{id}
DELETE /teachers/{id}

GET    /subjects
POST   /subjects
GET    /subjects/{id}
PATCH  /subjects/{id}
DELETE /subjects/{id}

GET    /groups
POST   /groups
GET    /groups/{id}
PATCH  /groups/{id}
DELETE /groups/{id}

GET    /rooms
POST   /rooms
GET    /rooms/{id}
PATCH  /rooms/{id}
DELETE /rooms/{id}

GET    /time-blocks
POST   /time-blocks
```

## Disponibilidad y restricciones

```text
GET  /availability/teachers/{teacherId}
PUT  /availability/teachers/{teacherId}

GET    /constraints
POST   /constraints
PATCH  /constraints/{id}
DELETE /constraints/{id}
```

## IA

```text
POST /ai/constraints/parse
```

Request:

```json
{
  "text": "La profesora Ana no puede los martes y prefiere terminar antes de las 13:00"
}
```

Response:

```json
{
  "constraints": [
    {
      "type": "TEACHER_UNAVAILABLE_DAY",
      "severity": "HARD",
      "targetId": "teacher-id",
      "parameters": { "day": "TUESDAY" }
    }
  ],
  "warnings": []
}
```

## Horarios

```text
POST /schedules/generate
GET  /schedules
GET  /schedules/{id}
POST /schedules/{id}/review
POST /schedules/{id}/publish
POST /schedules/{id}/archive
```

## Respuesta de error

```json
{
  "error": {
    "code": "ROOM_CAPACITY_INVALID",
    "message": "El salón no tiene capacidad suficiente.",
    "details": {}
  }
}
```

## OpenAPI

FastAPI genera:

```text
/docs
/redoc
/openapi.json
```

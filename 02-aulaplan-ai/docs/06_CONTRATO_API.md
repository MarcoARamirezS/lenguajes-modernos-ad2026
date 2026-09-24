[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Modelo Firestore](./05_MODELO_FIRESTORE.md) · [Arquitectura →](./07_ARQUITECTURA_PYTHON_FIREBASE_NETLIFY.md)

# 06 — Contrato API

## Base

```text
/api
```

## Health

```text
GET /api/health
```

Respuesta:

```json
{
  "status": "ok",
  "service": "aulaplan-api",
  "runtime": "python"
}
```

## Catálogos

```text
GET    /api/teachers
POST   /api/teachers
GET    /api/teachers/:id
PUT    /api/teachers/:id
DELETE /api/teachers/:id
```

El mismo patrón aplica a:

```text
subjects
groups
rooms
time-blocks
academic-periods
```

## Scheduling

```text
POST /api/schedules/generate
GET  /api/schedules
GET  /api/schedules/:id
POST /api/schedules/:id/publish
```

## IA

```text
POST /api/ai/constraints/parse
```

## Códigos

- 200 OK
- 201 Created
- 400 invalid request
- 401 unauthenticated
- 403 forbidden
- 404 not found
- 409 business conflict
- 422 validation error
- 500 unexpected error

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Modelo Firestore](./05_MODELO_FIRESTORE.md) · [Arquitectura →](./07_ARQUITECTURA_PYTHON_FIREBASE_NETLIFY.md)

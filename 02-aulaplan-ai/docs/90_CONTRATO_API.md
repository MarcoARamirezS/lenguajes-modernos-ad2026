[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 15](./SESION_15_TESTING_CICD_DEPLOY.md) · [Modelo Firestore →](./91_MODELO_FIRESTORE.md)

# 90 — Contrato REST

Base local:

```text
http://127.0.0.1:5001/PROJECT_ID/us-central1/api
```

Base producción consumida por Nuxt:

```text
/api
```

## Público

```text
GET /health
```

## Identidad

```text
GET /auth/me
GET /users                 ADMIN
```

## CRUD académicos

```text
GET    /academic-periods
POST   /academic-periods
GET    /academic-periods/:id
PUT    /academic-periods/:id
DELETE /academic-periods/:id

/teachers
/subjects
/groups
/rooms
/time-blocks
/offerings
/availability
/constraints
```

GET requiere usuario autenticado desde la Sesión 08. Escritura requiere `ADMIN` o `COORDINATOR`.

## IA

```text
POST /ai/constraints/parse
```

Request:

```json
{
  "text": "Ana no puede dar clases el martes."
}
```

## Horarios

```text
GET  /schedules
POST /schedules/generate
POST /schedules/:id/publish
```

Generate:

```json
{
  "academic_period_id": "PERIOD_ID",
  "max_nodes": 50000
}
```

## Códigos

| Código | Uso |
| ---: | --- |
| 200 | lectura/actualización |
| 201 | creación |
| 204 | delete |
| 401 | sin autenticación |
| 403 | rol insuficiente |
| 404 | recurso |
| 409 | conflicto/no solución |
| 422 | Pydantic |
| 500 | error inesperado |

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 15](./SESION_15_TESTING_CICD_DEPLOY.md) · [Modelo Firestore →](./91_MODELO_FIRESTORE.md)

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Contrato API](./90_CONTRATO_API.md) · [Seguridad →](./92_VARIABLES_SEGURIDAD.md)

# 91 — Modelo Firestore

## Colecciones

```text
users
academic_periods
teachers
subjects
groups
rooms
time_blocks
course_offerings
teacher_availability
constraints
schedules
```

## Relaciones

```text
academic_period
  ├── groups
  └── course_offerings
        ├── subject
        ├── group
        └── teacher
```

## Schedule

```text
schedules/{id}
└── versions/{version}
```

## `users/{uid}`

```json
{
  "email": "admin@example.com",
  "display_name": "Administrador",
  "role": "ADMIN",
  "active": true
}
```

## IDs

- `users`: Firebase UID.
- Catálogos: IDs Firestore.
- `time_blocks`: se recomienda ID legible en seeds, por ejemplo `MON-01`.
- `versions`: `v001`, `v002`, etc.

## Reglas de acceso

El navegador no tiene acceso administrativo directo a colecciones de negocio. Nuxt usa Firebase Auth para identidad y el backend Python usa Firebase Admin para datos.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Contrato API](./90_CONTRATO_API.md) · [Seguridad →](./92_VARIABLES_SEGURIDAD.md)

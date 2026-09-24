[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Inicio rápido](./00_INICIO_RAPIDO.md) · [Instalación →](./02_INSTALACION_MAC_LINUX_WINDOWS.md)

# 01 — Mapa del proyecto

## Arquitectura funcional

```text
Usuario
  ↓
Nuxt 4
  ↓
/api/*
  ↓
Netlify reverse proxy
  ↓
Firebase Function: api
  ↓
Flask Router
  ├── /health
  ├── /teachers
  ├── /subjects
  ├── /groups
  ├── /rooms
  ├── /constraints
  ├── /schedules
  └── /ai
        ↓
Services
        ↓
Repositories
        ↓
Firestore
```

## Módulos

1. Academic periods
2. Teachers
3. Subjects
4. Groups
5. Rooms
6. Time blocks
7. Availability
8. Constraints
9. Schedules
10. AI constraint parser
11. Users/RBAC

## Scheduler

```text
Input
 ↓
Validación
 ↓
Candidates
 ↓
Hard constraints
 ↓
Backtracking
 ↓
Soft constraints
 ↓
Score
 ↓
Best solution
```

## Despliegue

El repositorio es único, pero existen dos runtimes:

- Nuxt 4: Netlify.
- Python: Cloud Functions for Firebase.

Netlify mantiene `/api/*` como ruta pública mediante proxy.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Inicio rápido](./00_INICIO_RAPIDO.md) · [Instalación →](./02_INSTALACION_MAC_LINUX_WINDOWS.md)

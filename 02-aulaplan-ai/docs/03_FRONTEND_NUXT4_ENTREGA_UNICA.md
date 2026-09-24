[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación](./02_INSTALACION_MAC_LINUX_WINDOWS.md) · [Git y GitHub →](./04_GIT_GITHUB_WORKFLOW.md)

# 03 — Frontend Nuxt 4 — entrega única

## Regla

El frontend se entrega completo al inicio. Las sesiones posteriores se concentran en Python y Firebase.

## Stack

- Nuxt 4
- Vue 3
- TypeScript strict
- Composition API
- Pinia
- Tailwind CSS 4
- daisyUI

## Rutas

```text
/login
/dashboard
/teachers
/subjects
/groups
/rooms
/time-blocks
/availability
/constraints
/schedules
/schedules/new
/schedules/:id
/generator
/users
/settings
```

## API client

El frontend solo conoce una base:

```text
/api
```

En producción Netlify proxifica esta ruta hacia Firebase Functions.

En desarrollo puede configurarse:

```env
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5001/PROJECT_ID/us-central1/api
```

y en producción:

```env
NUXT_PUBLIC_API_BASE_URL=/api
```

## Auth

Firebase Auth se utiliza en el cliente para iniciar sesión y obtener un ID token.

Las operaciones de negocio pasan por el backend Python.

## Contrato

```text
Component
  ↓
Store / composable
  ↓
API service
  ↓
HTTP
  ↓
Python backend
```

No colocar lógica del scheduler en Vue.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación](./02_INSTALACION_MAC_LINUX_WINDOWS.md) · [Git y GitHub →](./04_GIT_GITHUB_WORKFLOW.md)

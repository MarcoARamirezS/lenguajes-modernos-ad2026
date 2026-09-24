[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Proyecto](../README.md) · [Mapa del proyecto →](./01_MAPA_DEL_PROYECTO.md)

# 00 — Inicio rápido

## Qué vas a construir

AulaPlan AI genera horarios académicos a partir de profesores, materias, grupos, salones, disponibilidad y restricciones.

## Qué aprenderás

- backend Python;
- funciones HTTP serverless;
- Firebase Admin y Firestore;
- autenticación y RBAC;
- validación con Pydantic;
- arquitectura por capas;
- algoritmos de backtracking;
- heurísticas y scoring;
- Gemini API;
- testing;
- CI/CD.

## Flujo principal

```text
Nuxt 4
  ↓ /api/*
Netlify proxy
  ↓
Firebase HTTP Function (Python)
  ↓
Router Flask
  ↓
Service
  ↓
Repository
  ↓
Firestore

Generar horario
  ↓
SchedulingService
  ↓
Backtracking
  ↓
Scoring
  ↓
Guardar versión
```

## Antes de empezar

Instala:

- Node.js 24 LTS;
- npm;
- Python 3.11;
- Git;
- Firebase CLI;
- Java 21 para Emulator Suite;
- cuenta de GitHub;
- cuenta de Netlify;
- proyecto Firebase.

## Orden

No saltes directamente al scheduler. Primero termina el dominio académico y las restricciones.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Proyecto](../README.md) · [Mapa del proyecto →](./01_MAPA_DEL_PROYECTO.md)

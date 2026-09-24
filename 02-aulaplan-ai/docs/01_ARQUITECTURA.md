[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Inicio aquí](./00_INICIO_AQUI.md) · [Requisitos →](./02_REQUISITOS.md)

# 01 — Arquitectura

## Producción

```text
                    GitHub
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
      Netlify               Firebase Functions
      Nuxt 4                   Python 3.11
         │                         │
         └── /api/* proxy ─────────┤
                                   │
                      ┌────────────┼────────────┐
                      ▼            ▼            ▼
                  Firestore       Auth        Gemini
                                   │
                                   ▼
                              Scheduler
```

## Capas backend

```text
HTTP Route
   ↓
Pydantic Schema
   ↓
Service
   ↓
Repository
   ↓
Firebase Admin / Firestore
```

El scheduler se mantiene como dominio Python puro para que pueda probarse sin Firebase.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Inicio aquí](./00_INICIO_AQUI.md) · [Requisitos →](./02_REQUISITOS.md)

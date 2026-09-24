# Lenguajes Modernos AD2026

Repositorio guía de la materia **Lenguajes Modernos**.

> **Empieza aquí:** [Guía de navegación del repositorio](./GUIA_DE_NAVEGACION.md)

## Proyectos

| Proyecto | Backend | Frontend | Datos / servicios | Guía |
| --- | --- | --- | --- | --- |
| 01 — E-Commerce Monorepo | Node.js + Express | Nuxt 4 | Firebase | [Abrir proyecto](./01-ecommerce-monorepo/README.md) |
| 02 — AulaPlan AI | **Python + Cloud Functions for Firebase** | Nuxt 4 | Firestore, Auth, Gemini | [Abrir proyecto](./02-aulaplan-ai/README.md) |

## Proyecto 02 — AulaPlan AI

AulaPlan AI es el proyecto evolutivo orientado a backend Python. El frontend se entrega una sola vez y el trabajo posterior se concentra en:

- Python;
- funciones HTTP serverless;
- Firebase Admin;
- Firestore;
- Firebase Authentication;
- Pydantic;
- arquitectura por capas;
- generación de horarios mediante backtracking;
- heurísticas y scoring;
- Gemini API;
- testing;
- GitHub;
- Netlify para el frontend;
- Cloud Functions for Firebase para el runtime Python.

### Aclaración de despliegue

Netlify se mantiene como hosting del frontend y como URL pública principal, pero **Netlify Functions no ofrece runtime Python**. Para conservar un backend Python real, la API se ejecuta como **Cloud Functions for Firebase en Python** y Netlify proxifica `/api/*` hacia esa función.

Esto permite que el frontend consuma:

```text
https://TU-SITIO.netlify.app/api/*
```

aunque el runtime Python sea administrado por Firebase.

## Estructura

```text
lenguajes-modernos-ad2026/
├── README.md
├── GUIA_DE_NAVEGACION.md
├── 01-ecommerce-monorepo/
│   ├── README.md
│   └── docs/
└── 02-aulaplan-ai/
    ├── README.md
    └── docs/
```

## Navegación rápida

### General

- [Guía de navegación](./GUIA_DE_NAVEGACION.md)
- [Proyecto 01](./01-ecommerce-monorepo/README.md)
- [Proyecto 02 — AulaPlan AI](./02-aulaplan-ai/README.md)

### AulaPlan AI

- [Índice de documentación](./02-aulaplan-ai/docs/README.md)
- [Inicio rápido](./02-aulaplan-ai/docs/00_INICIO_RAPIDO.md)
- [Instalación](./02-aulaplan-ai/docs/02_INSTALACION_MAC_LINUX_WINDOWS.md)
- [Frontend único](./02-aulaplan-ai/docs/03_FRONTEND_NUXT4_ENTREGA_UNICA.md)
- [Arquitectura Python/Firebase/Netlify](./02-aulaplan-ai/docs/07_ARQUITECTURA_PYTHON_FIREBASE_NETLIFY.md)
- [Sesión 01](./02-aulaplan-ai/docs/SESION_01_FOUNDATION_MONOREPO_PYTHON.md)

## Reglas del repositorio

- No subir `.env`.
- No subir credenciales de cuentas de servicio.
- No subir `node_modules`, `.venv`, `__pycache__` ni artefactos locales.
- Cada sesión debe cerrar con una validación funcional y un commit.
- La documentación debe indicar siempre el documento anterior y siguiente.

# Proyecto 02 — AulaPlan AI

**AulaPlan AI** es un generador inteligente de horarios académicos diseñado como proyecto evolutivo para **Lenguajes Modernos AD2026**.

La prioridad del proyecto es backend, Firebase, arquitectura serverless, algoritmos de planificación e integración de IA. El frontend se entrega una sola vez y después permanece estable mientras las sesiones conectan funcionalidad real.

## Decisión de arquitectura

Todo se despliega desde **un único monorepo** hacia **un único proyecto Netlify**:

```text
GitHub monorepo
       │
       ▼
    Netlify
       │
       ├── Nuxt 4 estático
       │      └── /
       │
       └── Netlify Functions TypeScript
              └── /api/*
                      │
                      ├── Firebase Auth
                      ├── Firestore
                      ├── Scheduler propio
                      └── Gemini API
```

No se utiliza Render, Railway, Vercel ni otro hosting para el backend.

## Stack

| Capa | Tecnología |
| --- | --- |
| Monorepo | npm Workspaces |
| Frontend | Nuxt 4 + Vue 3 + TypeScript |
| State | Pinia |
| UI | Tailwind CSS 4 + daisyUI |
| Backend | Netlify Functions modernas `.mts` |
| Contratos | TypeScript + Zod |
| Auth | Firebase Authentication |
| DB | Cloud Firestore |
| Backend Firebase | Firebase Admin SDK |
| Scheduling | Backtracking + heurísticas + scoring |
| IA | Gemini API con `@google/genai` |
| Unit/API tests | Vitest |
| E2E | Playwright |
| Deploy | Netlify |
| CI | GitHub Actions + Netlify Continuous Deployment |

## Por qué no se usa Go en esta versión

Netlify aún permite Go mediante su API compatible con AWS Lambda, pero ese modo fue marcado como **deprecated** y Netlify indica que dejará de aceptar despliegues en ese modo a partir del **1 de julio de 2027**. Para una guía nueva se utiliza la API moderna de Netlify Functions con TypeScript.

Esto evita enseñar una arquitectura con fecha de retiro próxima y permite centrar la novedad de la materia en:

- serverless moderno;
- Web `Request` / `Response`;
- arquitectura sin Express;
- Firebase Admin;
- diseño de un motor de horarios;
- backtracking y heurísticas;
- IA estructurada;
- CI/CD en un único proveedor.

## Estructura técnica objetivo

```text
aulaplan-ai/
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── public/
│   │   ├── nuxt.config.ts
│   │   └── package.json
│   └── api/
│       ├── netlify/
│       │   └── functions/
│       │       └── api.mts
│       ├── src/
│       │   ├── ai/
│       │   ├── auth/
│       │   ├── core/
│       │   ├── firebase/
│       │   ├── repositories/
│       │   ├── router/
│       │   ├── scheduler/
│       │   └── services/
│       ├── tests/
│       └── package.json
├── packages/
│   └── contracts/
├── firebase/
│   ├── firebase.json
│   ├── firestore.indexes.json
│   └── firestore.rules
├── docs/
├── .github/workflows/
├── .nvmrc
├── .gitignore
├── netlify.toml
├── package.json
└── README.md
```

## Sesiones

| # | Tema | Resultado |
| ---: | --- | --- |
| 01 | Foundation monorepo + Netlify | Proyecto ejecutándose desde cero |
| 02 | Functions modernas y arquitectura | `/api/health` + router modular |
| 03 | Firebase | Auth/Firestore/Emulators conectados |
| 04 | Academic Core | Periodos, profesores, materias |
| 05 | Recursos | Grupos, salones, bloques |
| 06 | Disponibilidad | Disponibilidad y restricciones |
| 07 | Seguridad | Firebase Auth + RBAC |
| 08 | Scheduling Domain | Problema de horarios modelado |
| 09 | Scheduler I | Backtracking funcional |
| 10 | Scheduler II | Heurísticas y scoring |
| 11 | IA | Gemini interpreta restricciones |
| 12 | Generación | Versionado y publicación |
| 13 | QA | Unit, API, Emulator y E2E |
| 14 | CI/CD | GitHub + Netlify producción |

## Documentación

[Ir al índice de documentación](./docs/README.md)

## Criterio de cierre

El proyecto termina cuando un coordinador puede:

1. autenticarse;
2. administrar catálogos académicos;
3. capturar disponibilidades y restricciones;
4. solicitar la generación de un horario;
5. recibir una solución sin conflictos duros;
6. comparar calidad mediante scoring;
7. interpretar restricciones escritas en lenguaje natural mediante IA;
8. guardar versiones;
9. publicar un horario;
10. usar la aplicación completa desde una sola URL de Netlify.

[Volver al índice general](../README.md)

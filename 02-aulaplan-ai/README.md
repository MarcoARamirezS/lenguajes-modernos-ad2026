# Proyecto 02 — AulaPlan AI

[← Repositorio](../README.md) · [Guía general](../GUIA_DE_NAVEGACION.md) · [Índice de documentación](./docs/README.md)

**AulaPlan AI** es un generador inteligente de horarios académicos desarrollado como proyecto evolutivo.

## Objetivo académico

El frontend se entrega completo al inicio. Las sesiones se concentran en un backend **Python** y en la integración con Firebase.

## Stack definitivo

| Capa | Tecnología |
| --- | --- |
| Frontend | Nuxt 4 + Vue 3 + TypeScript |
| Estado | Pinia |
| UI | Tailwind CSS 4 + daisyUI |
| Backend | **Python 3.11** |
| Runtime backend | **Cloud Functions for Firebase (Python)** |
| Router HTTP | Flask app expuesta por una HTTP Function |
| Validación | Pydantic |
| Auth | Firebase Authentication |
| DB | Cloud Firestore |
| Admin | Firebase Admin SDK para Python |
| IA | Gemini API con `google-genai` |
| Scheduler | Python: backtracking + heurísticas + scoring |
| Tests backend | pytest |
| E2E | Playwright |
| Front deploy | Netlify |
| Backend deploy | Firebase Functions |
| Repositorio | GitHub monorepo |

## Arquitectura

```text
GitHub monorepo
       │
       ├──────────────────────────────┐
       │                              │
       ▼                              ▼
    Netlify                    Firebase Functions
  Nuxt 4 SPA                     Python 3.11
       │                              │
       │ /api/*                       │
       └──────── Netlify proxy ───────┤
                                      │
                       ┌──────────────┼──────────────┐
                       ▼              ▼              ▼
                   Firestore         Auth          Gemini

                                      ▼
                               Scheduler Python
```

## Por qué no se ejecuta Python dentro de Netlify

Netlify dispone de Python en su entorno de **build**, pero sus Functions modernas no tienen runtime Python. Por ello, una guía que afirmara que FastAPI o un backend Python corre como Netlify Function sería incorrecta.

Para mantener el objetivo pedagógico de Python:

- el frontend se despliega en Netlify;
- el backend Python se despliega en Cloud Functions for Firebase;
- Netlify proxifica `/api/*`;
- el frontend usa una única ruta `/api`;
- todo el código vive en el mismo monorepo.

## Estructura objetivo

```text
aulaplan-ai/
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── public/
│   │   ├── nuxt.config.ts
│   │   └── package.json
│   └── api/
│       ├── main.py
│       ├── requirements.txt
│       ├── .python-version
│       ├── src/
│       │   ├── ai/
│       │   ├── auth/
│       │   ├── core/
│       │   ├── firebase/
│       │   ├── http/
│       │   ├── repositories/
│       │   ├── scheduler/
│       │   ├── schemas/
│       │   └── services/
│       └── tests/
├── firebase/
│   ├── firestore.rules
│   └── firestore.indexes.json
├── docs/
├── .github/workflows/
├── firebase.json
├── netlify.toml
├── package.json
└── README.md
```

## Ruta recomendada

1. [Inicio rápido](./docs/00_INICIO_RAPIDO.md)
2. [Mapa del proyecto](./docs/01_MAPA_DEL_PROYECTO.md)
3. [Instalación](./docs/02_INSTALACION_MAC_LINUX_WINDOWS.md)
4. [Frontend único](./docs/03_FRONTEND_NUXT4_ENTREGA_UNICA.md)
5. [Arquitectura Python/Firebase/Netlify](./docs/07_ARQUITECTURA_PYTHON_FIREBASE_NETLIFY.md)
6. [Sesión 01](./docs/SESION_01_FOUNDATION_MONOREPO_PYTHON.md)

## Sesiones

| Sesión | Tema |
| ---: | --- |
| 01 | Monorepo + Python + Nuxt + Firebase CLI |
| 02 | Arquitectura backend Python |
| 03 | Firebase Functions + Firestore + Emulators |
| 04 | Academic Core |
| 05 | Groups, Rooms & Time Blocks |
| 06 | Availability & Constraints |
| 07 | Firebase Auth + RBAC |
| 08 | Scheduling Domain |
| 09 | Backtracking |
| 10 | Heurísticas + scoring |
| 11 | Gemini con Python |
| 12 | Generación + versionado |
| 13 | Testing + QA |
| 14 | GitHub + Netlify + Firebase deployment |

[Continuar → Índice de documentación](./docs/README.md)

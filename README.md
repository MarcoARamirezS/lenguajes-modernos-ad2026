# Lenguajes Modernos AD2026

Repositorio general de la materia **Lenguajes Modernos**.

Aquí se concentran los proyectos, prácticas, guías de instalación, evidencias y documentación técnica que se desarrollarán durante el curso.

## Propósito del repositorio

Este repositorio funciona como punto de entrada para todos los proyectos de la materia. Cada proyecto tiene su propia carpeta, su `README.md` y una carpeta `docs` con sesiones, guías técnicas y material de apoyo.

## Objetivo de la materia

Desarrollar aplicaciones modernas aplicando lenguajes, frameworks, herramientas, APIs y flujos de trabajo utilizados en proyectos profesionales.

Durante el curso se trabaja con:

- Git y GitHub.
- Desarrollo frontend moderno.
- APIs REST.
- Arquitectura modular.
- Monorepos.
- Autenticación y autorización.
- Persistencia NoSQL.
- Pruebas automatizadas.
- Documentación técnica.
- Despliegue continuo.
- Python para backend.
- Optimización matemática.
- Integración responsable de IA generativa.

## Proyectos

| Proyecto | Enfoque | Carpeta |
| --- | --- | --- |
| Proyecto 01 | E-commerce con Node.js, Express, Nuxt 4 y Firestore | [`01-ecommerce-monorepo`](./01-ecommerce-monorepo/README.md) |
| Proyecto 02 | AulaPlan AI: FastAPI, Firebase, OR-Tools, Gemini y Nuxt 4 | [`02-aulaplan-ai`](./02-aulaplan-ai/README.md) |

## Evolución didáctica

```text
Proyecto 01
Node.js + Express + REST + Firestore
             │
             ▼
Proyecto 02
Python + FastAPI + Firebase
             │
             ├── optimización con OR-Tools
             ├── IA generativa con Gemini
             ├── testing con Pytest
             └── CI/CD con GitHub, Netlify y Render
```

## Stack general del curso

| Área | Herramientas |
| --- | --- |
| Control de versiones | Git, GitHub |
| Frontend | Nuxt 4, Vue 3, TypeScript strict |
| Estado | Pinia |
| Estilos | Tailwind CSS 4, daisyUI 5 |
| Backend Proyecto 01 | Node.js, Express, Zod |
| Backend Proyecto 02 | Python 3.12, FastAPI, Pydantic |
| Base de datos | Firebase Cloud Firestore |
| Autenticación | Firebase Authentication / JWT según proyecto |
| Optimización | Google OR-Tools CP-SAT |
| IA | Gemini API |
| Pruebas | Vitest, Supertest, Pytest, HTTPX, Playwright |
| Deploy frontend | Netlify |
| Deploy backend Python | Render |
| Documentación | Markdown, OpenAPI / Swagger |

## Estructura del repositorio

```text
lenguajes-modernos-ad2026/
├── README.md
├── 01-ecommerce-monorepo/
│   ├── README.md
│   └── docs/
└── 02-aulaplan-ai/
    ├── README.md
    └── docs/
```

## Convención de trabajo

Cada proyecto debe incluir:

- `README.md` del proyecto.
- Carpeta `docs`.
- Mapa técnico.
- Guía de instalación.
- Sesiones de 1 hora 30 minutos.
- Comandos verificables.
- Checklist de cierre.
- Commit sugerido.

## Flujo Git sugerido

Crear una rama por sesión o bloque funcional:

```bash
git switch -c feature/sesion-01-foundation
```

Guardar cambios:

```bash
git status
git add .
git commit -m "chore: complete session 01 foundation"
```

Subir cambios:

```bash
git push -u origin feature/sesion-01-foundation
```

## Reglas importantes

- No subir `node_modules`.
- No subir `.venv`.
- No subir archivos `.env`.
- No subir llaves JSON de cuentas de servicio.
- Mantener actualizados los README.
- Ejecutar verificaciones antes de cada entrega.
- No guardar claves de Gemini ni Firebase en el código.

## Navegación rápida

### Proyecto 01

- [E-Commerce Monorepo](./01-ecommerce-monorepo/README.md)
- [Documentación Proyecto 01](./01-ecommerce-monorepo/docs/README.md)

### Proyecto 02

- [AulaPlan AI](./02-aulaplan-ai/README.md)
- [Documentación AulaPlan AI](./02-aulaplan-ai/docs/README.md)
- [Mapa de AulaPlan AI](./02-aulaplan-ai/docs/00_MAPA_DEL_PROYECTO.md)
- [Instalación y ejecución](./02-aulaplan-ai/docs/01_INSTALACION_Y_EJECUCION.md)
- [Frontend Nuxt 4 — entrega única](./02-aulaplan-ai/docs/02_FRONTEND_NUXT4_ENTREGA_UNICA.md)

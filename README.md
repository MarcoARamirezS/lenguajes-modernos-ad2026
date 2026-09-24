# Lenguajes Modernos AD2026

Repositorio general de la materia **Lenguajes Modernos**.

Aquí se concentran los proyectos, prácticas, guías de instalación, evidencias y documentación técnica que se desarrollarán durante el curso.

## Propósito del repositorio

Este repositorio funciona como punto de entrada para todos los proyectos de la materia. Cada proyecto tendrá su propia carpeta, su propio `README.md` y una carpeta `docs` con las sesiones, guías técnicas y material de apoyo.

## Objetivo de la materia

Desarrollar aplicaciones modernas aplicando lenguajes, frameworks, herramientas y flujos de trabajo usados actualmente en proyectos profesionales.

Durante el curso se trabajará con:

- Control de versiones con Git y GitHub.
- Desarrollo frontend moderno.
- Desarrollo backend con APIs REST.
- Arquitectura modular.
- Monorepos con npm Workspaces.
- Autenticación y autorización.
- Persistencia de datos.
- Consumo de APIs desde frontend.
- Pruebas básicas.
- Documentación técnica.
- Preparación para despliegue.

## Stack general del curso

| Área | Herramientas |
| --- | --- |
| Control de versiones | Git, GitHub |
| Runtime | Node.js LTS |
| Monorepo | npm Workspaces |
| Backend | Express, Zod, JWT, Firebase Admin SDK |
| Base de datos | Firestore |
| Frontend | Nuxt 4, Vue 3, TypeScript |
| Estado frontend | Pinia |
| Estilos | Tailwind CSS |
| Pruebas | Vitest, Supertest, Playwright |
| Documentación | Markdown, OpenAPI |

## Estructura del repositorio

```text
lenguajes-modernos-ad2026/
├── README.md
└── 01-ecommerce-monorepo/
    ├── README.md
    └── docs/
        ├── README.md
        ├── 00_MAPA_DEL_PROYECTO.md
        ├── 01_INSTALACION_Y_EJECUCION.md
        ├── 02_FRONTEND_NUXT4_GUIA.md
        ├── SESION_01_INSTALACION_FRONTEND.md
        ├── SESION_02_PRODUCTS_COMPLETO.md
        ├── SESION_03_AUTH_USERS_JWT.md
        ├── SESION_04_RBAC_RUTAS_PRIVADAS.md
        ├── SESION_05_CATEGORIES_CATALOGO.md
        ├── SESION_06_CART_ORDERS.md
        └── SESION_07_TESTING_OPENAPI_CIERRE.md
```

## Proyectos

| Proyecto | Descripción | Carpeta |
| --- | --- | --- |
| Proyecto 01 | E-commerce con backend, frontend y monorepo | [`01-ecommerce-monorepo`](./01-ecommerce-monorepo/README.md) |

## Convención de trabajo

Cada proyecto debe incluir:

- `README.md` del proyecto.
- Carpeta `docs`.
- Guías por sesión.
- Instrucciones de instalación.
- Checklist de entrega.
- Commits por avance.

## Flujo Git sugerido

Crear una rama por sesión o bloque funcional:

```bash
git switch -c feature/sesion-01-instalacion
```

Guardar cambios:

```bash
git status
git add .
git commit -m "docs: add session 01 installation guide"
```

Subir cambios:

```bash
git push origin feature/sesion-01-instalacion
```

## Criterios generales de entrega

Cada entrega debe incluir:

- Código fuente actualizado.
- Documentación correspondiente.
- Evidencia de ejecución.
- Commits claros.
- Capturas cuando se soliciten.
- Descripción breve de problemas encontrados y solución aplicada.

## Reglas importantes

- No subir `node_modules`.
- No subir archivos `.env`.
- Mantener actualizados los README.
- Usar nombres claros para carpetas, ramas y commits.
- Probar el proyecto antes de entregar.

## Navegación rápida

- [Proyecto 01 - E-Commerce Monorepo](./01-ecommerce-monorepo/README.md)
- [Documentación del Proyecto 01](./01-ecommerce-monorepo/docs/README.md)
- [Mapa del Proyecto 01](./01-ecommerce-monorepo/docs/00_MAPA_DEL_PROYECTO.md)
- [Instalación y ejecución](./01-ecommerce-monorepo/docs/01_INSTALACION_Y_EJECUCION.md)
- [Guía Frontend Nuxt 4](./01-ecommerce-monorepo/docs/02_FRONTEND_NUXT4_GUIA.md)


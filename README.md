# Lenguajes Modernos AD2026

Repositorio general de la materia **Lenguajes Modernos**.

Aquí se concentran los proyectos, prácticas, guías de instalación, evidencias y documentación técnica que se desarrollarán durante el curso.

## Propósito del repositorio

Cada proyecto tiene su propia carpeta, `README.md` y directorio `docs`. Las guías están pensadas para poder seguirse desde cero, con comandos verificables y cierres por sesión.

## Evolución de proyectos

| Proyecto | Enfoque principal | Tecnologías clave |
| --- | --- | --- |
| 01 | E-Commerce Full-Stack tradicional | Node.js, Express, Nuxt 4, Firebase |
| 02 | AulaPlan AI: serverless + algoritmos + IA | Nuxt 4, Netlify Functions, Firebase, Gemini |

## Stack general del curso

| Área | Herramientas |
| --- | --- |
| Control de versiones | Git, GitHub |
| Runtime principal | Node.js 24 LTS |
| Monorepo | npm Workspaces |
| Frontend | Nuxt 4, Vue 3, TypeScript |
| Estado | Pinia |
| UI | Tailwind CSS 4, daisyUI |
| Backend Proyecto 01 | Node.js + Express |
| Backend Proyecto 02 | Netlify Functions modernas + TypeScript |
| Persistencia | Firebase Authentication + Cloud Firestore |
| IA | Gemini API |
| Testing | Vitest, Playwright |
| Deploy Proyecto 02 | Un único proyecto Netlify |

## Estructura

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

## Proyectos

### Proyecto 01 — E-Commerce Monorepo

[Ir al Proyecto 01](./01-ecommerce-monorepo/README.md)

### Proyecto 02 — AulaPlan AI

Generador inteligente de horarios académicos con frontend Nuxt 4, backend serverless en Netlify Functions, Firebase y Gemini. Todo se despliega desde **un mismo monorepo a un único proyecto Netlify**.

[Ir al Proyecto 02](./02-aulaplan-ai/README.md)

## Convención de trabajo

Cada proyecto debe incluir:

- README del proyecto.
- Documentación por sesiones.
- Instalación para macOS, Linux y Windows.
- Checklist verificable.
- Flujo Git sugerido.
- Evidencia de pruebas.
- Variables de entorno documentadas mediante `.env.example`, nunca secretos reales.

## Flujo Git sugerido

```bash
git switch -c feature/sesion-01-foundation
git status
git add .
git commit -m "feat: complete session 01 foundation"
git push -u origin feature/sesion-01-foundation
```

## Reglas importantes

- No subir `node_modules`.
- No subir `.env`, credenciales Firebase ni API keys.
- No subir archivos de cuentas de servicio.
- Mantener README y documentación actualizados.
- Probar antes de hacer merge a `main`.
- Mantener una única fuente de verdad para contratos y tipos compartidos.

## Navegación rápida

- [Proyecto 01](./01-ecommerce-monorepo/README.md)
- [Proyecto 02 — AulaPlan AI](./02-aulaplan-ai/README.md)
- [Documentación AulaPlan AI](./02-aulaplan-ai/docs/README.md)
- [Instalación AulaPlan AI](./02-aulaplan-ai/docs/01_INSTALACION_Y_EJECUCION.md)
- [Frontend único AulaPlan AI](./02-aulaplan-ai/docs/02_FRONTEND_NUXT4_ENTREGA_UNICA.md)

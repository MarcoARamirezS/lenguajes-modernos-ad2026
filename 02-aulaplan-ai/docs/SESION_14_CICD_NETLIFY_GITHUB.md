# 14 — GitHub CI/CD y despliegue único en Netlify

**Duración:** 1 hora 30 minutos.

## Objetivo

Cerrar el proyecto con CI, variables seguras y un único deploy que publique frontend y backend serverless juntos.

## Distribución de tiempo

- **00–20 min** — GitHub Actions
- **20–40 min** — Netlify project
- **40–60 min** — Environment
- **60–75 min** — Deploy
- **75–90 min** — Smoke/UAT

## Conceptos

- continuous integration
- continuous deployment
- deploy preview
- environment variables
- production smoke test

## Desarrollo

### 1. CI

Crear workflow para `npm ci`, typecheck, lint y tests. El build debe ejecutarse desde raíz.

### 2. Conectar GitHub

En Netlify importar el repositorio completo. No seleccionar un repositorio separado para backend.

### 3. Build

Usar comando raíz `npm run generate:web`; publish `apps/web/.output/public`; functions `apps/api/netlify/functions`.

### 4. Variables

Configurar Firebase público para build/frontend y secretos Firebase Admin/Gemini para Functions. No pegar secretos en `netlify.toml`.

### 5. Deploy

Push a `main` activa un único deploy. Confirmar en los logs que se publicaron assets y Functions.

### 6. Smoke

Validar `/`, `/login`, `/api/health`, login, listado protegido y generación con dataset demo.

### 7. Rollback

Documentar cómo seleccionar un deploy anterior desde Netlify si una versión falla.

## Endpoints al cierre

- `GET /api/health`
- `Flujo completo de producción`

## Checklist de cierre

- [ ] Una sola URL Netlify
- [ ] Frontend carga
- [ ] API responde bajo `/api/*`
- [ ] Auth verifica token
- [ ] Generador crea horario
- [ ] CI verde antes de merge
- [ ] Sin secretos en Git

## Commit sugerido

```bash
git add .
git commit -m "ci: deploy AulaPlan AI entirely on Netlify"
```

## Nota técnica

El proyecto se considera terminado solo cuando no existe ninguna dependencia de hosting externo para ejecutar la aplicación web y su API.

## Workflow de CI

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm

      - name: Install
        run: npm ci

      - name: Typecheck API
        run: npm run typecheck --workspace @aulaplan/api

      - name: Test API
        run: npm run test --workspace @aulaplan/api

      - name: Generate frontend
        run: npm run generate:web
```

Agregar E2E en un job posterior cuando el dataset/emuladores estén automatizados.

## Configuración Netlify definitiva

```toml
[build]
  command = "npm run generate:web"
  publish = "apps/web/.output/public"
  functions = "apps/api/netlify/functions"

[build.environment]
  NODE_VERSION = "24"

[functions]
  node_bundler = "esbuild"
```

## Variables en Netlify

Frontend/build:

```text
NUXT_PUBLIC_FIREBASE_API_KEY
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NUXT_PUBLIC_FIREBASE_PROJECT_ID
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
NUXT_PUBLIC_FIREBASE_APP_ID
```

Functions:

```text
FIREBASE_PROJECT_ID
FIREBASE_CLIENT_EMAIL
FIREBASE_PRIVATE_KEY
GEMINI_API_KEY
GEMINI_MODEL
MAX_SOLVER_MS
```

## Smoke test de producción

### macOS/Linux

```bash
curl https://TU-SITIO.netlify.app/api/health
```

### Windows PowerShell

```powershell
Invoke-RestMethod https://TU-SITIO.netlify.app/api/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "service": "aulaplan-api"
}
```

Después validar login y un flujo real desde el navegador.

[Volver al índice](./README.md)

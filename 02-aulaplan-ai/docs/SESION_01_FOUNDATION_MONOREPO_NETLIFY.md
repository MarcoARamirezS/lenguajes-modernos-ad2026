# 01 — Foundation: monorepo, Nuxt 4 y Netlify

**Duración:** 1 hora 30 minutos.

## Objetivo

Crear AulaPlan AI desde cero, preparar el monorepo, instalar Nuxt 4, crear el workspace API serverless, configurar Netlify CLI y verificar frontend + `/api/health` bajo el mismo origen.

## Distribución de tiempo

- **00–15 min** — Arquitectura y restricciones
- **15–35 min** — Creación multiplataforma
- **35–55 min** — Workspaces y dependencias
- **55–75 min** — Nuxt + Function health
- **75–90 min** — Netlify Dev + Git

## Conceptos

- npm Workspaces
- Nuxt 4
- Netlify Functions modernas
- same-origin API
- Git desde el primer commit

## Desarrollo

### 1. Crear el proyecto en macOS/Linux

```bash
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
mkdir -p apps/web apps/api/netlify/functions apps/api/src packages/contracts/src firebase docs .github/workflows
```

### 2. Crear el proyecto en Windows PowerShell

```powershell
New-Item -ItemType Directory -Force aulaplan-ai | Out-Null
Set-Location aulaplan-ai
git init
npm init -y
New-Item -ItemType Directory -Force apps/web | Out-Null
New-Item -ItemType Directory -Force apps/api/netlify/functions | Out-Null
New-Item -ItemType Directory -Force apps/api/src | Out-Null
New-Item -ItemType Directory -Force packages/contracts/src | Out-Null
New-Item -ItemType Directory -Force firebase | Out-Null
New-Item -ItemType Directory -Force docs | Out-Null
New-Item -ItemType Directory -Force .github/workflows | Out-Null
```

### 3. Configurar workspaces

```bash
npm pkg set private=true --json
npm pkg set "workspaces[0]=apps/*" "workspaces[1]=packages/*"
npm create nuxt@latest apps/web
cd apps/api && npm init -y && cd ../..
cd packages/contracts && npm init -y && cd ../..
```

### 4. Instalar herramientas

```bash
npm install --workspace apps/api @netlify/functions zod
npm install --workspace apps/api -D typescript vitest @types/node
npm install -D netlify-cli firebase-tools concurrently
```

### 5. Crear Function health

Crear `apps/api/netlify/functions/api.mts`. Debe responder `GET /api/health` usando `Request` y `Response`, sin Express. Exportar configuración con `path: ["/api", "/api/*"]`.

### 6. Configurar netlify.toml

Desde la raíz definir `publish = "apps/web/.output/public"` y `functions = "apps/api/netlify/functions"`. En `[dev]`, ejecutar `npm run dev:web`, apuntar a `targetPort = 3000` y exponer Netlify Dev en `8888`.

### 7. Ejecutar

```bash
npx netlify dev
```
Validar `http://localhost:8888` y `http://localhost:8888/api/health`.

### 8. Primer commit

```bash
git branch -M main
git add .
git commit -m "chore: initialize AulaPlan AI monorepo"
```

## Endpoints al cierre

- `GET /api/health`

## Checklist de cierre

- [ ] Frontend visible en `localhost:8888`
- [ ] `/api/health` devuelve 200
- [ ] No existe servidor Express
- [ ] No existen secretos en Git
- [ ] Monorepo contiene `apps/web` y `apps/api`

## Commit sugerido

```bash
git add .
git commit -m "chore: initialize AulaPlan AI monorepo"
```

## Archivos de configuración de la sesión

### `package.json` raíz

Usar esta forma como referencia después de ejecutar los comandos de instalación:

```json
{
  "name": "aulaplan-ai",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "netlify dev",
    "dev:web": "npm run dev --workspace @aulaplan/web",
    "generate:web": "npm run generate --workspace @aulaplan/web",
    "typecheck": "npm run typecheck --workspace @aulaplan/api && npm run typecheck --workspace @aulaplan/web",
    "test": "npm run test --workspace @aulaplan/api"
  },
  "devDependencies": {
    "concurrently": "latest",
    "firebase-tools": "latest",
    "netlify-cli": "latest"
  }
}
```

### `apps/api/package.json`

```json
{
  "name": "@aulaplan/api",
  "private": true,
  "type": "module",
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```

Las dependencias se agregan mediante `npm install`, por lo que no es necesario copiar versiones manualmente.

### `apps/api/netlify/functions/api.mts`

Primera versión:

```ts
import type { Config, Context } from '@netlify/functions'

export default async (req: Request, _context: Context) => {
  const url = new URL(req.url)

  if (req.method === 'GET' && url.pathname === '/api/health') {
    return Response.json({
      status: 'ok',
      service: 'aulaplan-api'
    })
  }

  return Response.json(
    {
      error: {
        code: 'NOT_FOUND',
        message: 'Route not found'
      }
    },
    { status: 404 }
  )
}

export const config: Config = {
  path: ['/api', '/api/*']
}
```

### `netlify.toml`

```toml
[build]
  command = "npm run generate:web"
  publish = "apps/web/.output/public"
  functions = "apps/api/netlify/functions"

[build.environment]
  NODE_VERSION = "24"

[dev]
  command = "npm run dev:web"
  targetPort = 3000
  port = 8888
  autoLaunch = false

[functions]
  node_bundler = "esbuild"
```

### Prueba

```bash
npx netlify dev
```

En otra terminal:

```bash
curl http://localhost:8888/api/health
```

Windows PowerShell también puede usar:

```powershell
Invoke-RestMethod http://localhost:8888/api/health
```

[Volver al índice](./README.md)

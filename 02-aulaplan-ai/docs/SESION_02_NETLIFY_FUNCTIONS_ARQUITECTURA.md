# 02 — Netlify Functions modernas y arquitectura backend

**Duración:** 1 hora 30 minutos.

## Objetivo

Reemplazar un handler monolítico por una arquitectura serverless modular con router, validación, servicios, repositorios y respuestas estandarizadas.

## Distribución de tiempo

- **00–20 min** — Modelo de ejecución serverless
- **20–40 min** — Router interno
- **40–60 min** — Responses y errores
- **60–75 min** — Zod
- **75–90 min** — Pruebas

## Conceptos

- stateless functions
- Request/Response Web API
- routing
- Zod
- error envelope
- dependency boundaries

## Desarrollo

### 1. Estructura backend

Crear `apps/api/src/core`, `router`, `services`, `repositories` y `schemas`. La Function `api.mts` solo adapta la invocación y delega al router.

### 2. Router

El router debe analizar `new URL(req.url).pathname`, método HTTP y parámetros. No debe contener acceso directo a Firestore.

### 3. Responses

Crear helpers JSON para `200`, `201`, `204`, errores `400/401/403/404/409/422/500` y encabezado `content-type: application/json`.

### 4. Info endpoint

Implementar `GET /api/info` con nombre, versión y ambiente, sin exponer secretos.

### 5. Validación

Crear un endpoint de ejemplo que valide body con Zod y devuelva el envelope de error acordado.

### 6. Pruebas

Probar router y helpers sin iniciar un servidor HTTP persistente. La lógica debe ser invocable como funciones puras siempre que sea posible.

## Endpoints al cierre

- `GET /api/health`
- `GET /api/info`

## Checklist de cierre

- [ ] Router separado de la Function
- [ ] Errores tienen formato único
- [ ] Body inválido devuelve 400/422 según contrato
- [ ] Tests de router en verde

## Commit sugerido

```bash
git add .
git commit -m "feat: implement serverless API foundation"
```

## Código base de arquitectura

### `apps/api/src/core/errors.ts`

```ts
export class AppError extends Error {
  constructor(
    public readonly statusCode: number,
    public readonly code: string,
    message: string,
    public readonly details?: unknown
  ) {
    super(message)
    this.name = 'AppError'
  }
}
```

### `apps/api/src/core/http.ts`

```ts
import { AppError } from './errors'

export function json(data: unknown, status = 200) {
  return Response.json(data, { status })
}

export function noContent() {
  return new Response(null, { status: 204 })
}

export async function readJson<T>(req: Request): Promise<T> {
  try {
    return await req.json() as T
  } catch {
    throw new AppError(400, 'INVALID_JSON', 'Request body must be valid JSON')
  }
}

export function errorResponse(error: unknown) {
  if (error instanceof AppError) {
    return json({
      error: {
        code: error.code,
        message: error.message,
        details: error.details
      }
    }, error.statusCode)
  }

  console.error(error)

  return json({
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'Internal server error'
    }
  }, 500)
}
```

### `apps/api/src/core/router.ts`

```ts
import { json } from './http'

type Params = Record<string, string>
type Handler = (req: Request, params: Params) => Promise<Response>

type Route = {
  method: string
  pattern: string
  handler: Handler
}

function segments(value: string) {
  return value.split('/').filter(Boolean)
}

function match(pattern: string, pathname: string): Params | null {
  const expected = segments(pattern)
  const actual = segments(pathname)

  if (expected.length !== actual.length) {
    return null
  }

  const params: Params = {}

  for (let i = 0; i < expected.length; i += 1) {
    const left = expected[i]
    const right = actual[i]

    if (left.startsWith(':')) {
      params[left.slice(1)] = decodeURIComponent(right)
      continue
    }

    if (left !== right) {
      return null
    }
  }

  return params
}

export class Router {
  private readonly routes: Route[] = []

  on(method: string, pattern: string, handler: Handler) {
    this.routes.push({
      method: method.toUpperCase(),
      pattern,
      handler
    })
  }

  get(pattern: string, handler: Handler) {
    this.on('GET', pattern, handler)
  }

  post(pattern: string, handler: Handler) {
    this.on('POST', pattern, handler)
  }

  put(pattern: string, handler: Handler) {
    this.on('PUT', pattern, handler)
  }

  delete(pattern: string, handler: Handler) {
    this.on('DELETE', pattern, handler)
  }

  async dispatch(req: Request) {
    const url = new URL(req.url)
    const pathname = url.pathname.replace(/^\/api/, '') || '/'

    for (const route of this.routes) {
      if (route.method !== req.method.toUpperCase()) {
        continue
      }

      const params = match(route.pattern, pathname)

      if (params) {
        return await route.handler(req, params)
      }
    }

    return json({
      error: {
        code: 'NOT_FOUND',
        message: 'Route not found'
      }
    }, 404)
  }
}
```

### `apps/api/src/routes/system.routes.ts`

```ts
import type { Router } from '../core/router'
import { json } from '../core/http'

export function registerSystemRoutes(router: Router) {
  router.get('/health', async () => {
    return json({
      status: 'ok',
      service: 'aulaplan-api'
    })
  })

  router.get('/info', async () => {
    return json({
      name: 'AulaPlan AI',
      version: '0.1.0',
      runtime: 'netlify-functions'
    })
  })
}
```

### `apps/api/src/app.ts`

```ts
import { errorResponse } from './core/http'
import { Router } from './core/router'
import { registerSystemRoutes } from './routes/system.routes'

const router = new Router()

registerSystemRoutes(router)

export async function handleApiRequest(req: Request) {
  try {
    return await router.dispatch(req)
  } catch (error) {
    return errorResponse(error)
  }
}
```

### `apps/api/netlify/functions/api.mts`

```ts
import type { Config, Context } from '@netlify/functions'
import { handleApiRequest } from '../../src/app'

export default async (req: Request, _context: Context) => {
  return await handleApiRequest(req)
}

export const config: Config = {
  path: ['/api', '/api/*']
}
```

[Volver al índice](./README.md)

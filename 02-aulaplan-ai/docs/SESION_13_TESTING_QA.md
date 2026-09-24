# 13 — Testing y QA

**Duración:** 1 hora 30 minutos.

## Objetivo

Crear una pirámide de pruebas enfocada en reglas del scheduler, API serverless, Firebase Emulator y flujos E2E.

## Distribución de tiempo

- **00–20 min** — Test strategy
- **20–45 min** — Unit scheduler
- **45–60 min** — API
- **60–75 min** — Emulator integration
- **75–90 min** — Playwright

## Conceptos

- unit tests
- integration tests
- Firebase Emulator
- API contract
- E2E

## Desarrollo

### 1. Unit

Probar capacidad, disponibilidad, conflictos, apply/rollback, scoring, deadline y heurísticas.

### 2. API

Invocar router con `Request` reales construidos en test. Validar status, headers y error envelope.

### 3. Firebase

Ejecutar repositories contra Firestore Emulator. Limpiar datos entre suites.

### 4. Auth

Cubrir 401/403 y roles permitidos. Usar Emulator cuando el alcance lo permita.

### 5. E2E

Playwright: login → catálogos → restricciones → generar → revisar → publicar.

### 6. Quality gate

No hacer deploy si unit/API fallan. Mantener fixtures pequeños para CI.

## Endpoints al cierre

- `Todos los endpoints críticos`

## Checklist de cierre

- [ ] Scheduler unit tests verdes
- [ ] Repositories contra Emulator verdes
- [ ] Auth cases verdes
- [ ] E2E crítico verde
- [ ] No se requiere Firebase producción para CI

## Commit sugerido

```bash
git add .
git commit -m "test: complete AulaPlan AI quality gates"
```

## Configuración Vitest

### `apps/api/vitest.config.ts`

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    clearMocks: true
  }
})
```

## Test del router

```ts
import { describe, expect, it } from 'vitest'
import { handleApiRequest } from '../src/app'

describe('system routes', () => {
  it('GET /api/health returns ok', async () => {
    const req = new Request('http://localhost/api/health')
    const response = await handleApiRequest(req)

    expect(response.status).toBe(200)
    expect(await response.json()).toEqual({
      status: 'ok',
      service: 'aulaplan-api'
    })
  })
})
```

## Test de regla dura

```ts
import { describe, expect, it } from 'vitest'

it('does not allow the same teacher in the same time block', () => {
  const busy = new Set(['teacher-1:block-1'])
  expect(busy.has('teacher-1:block-1')).toBe(true)
})
```

En el código real probar `canPlace` como función exportable/pura o mediante un módulo de reglas, no copiando la lógica dentro del test.

## CI con emuladores

Para integration tests usar Firebase Emulator Suite. La suite no debe depender de Firestore producción.

Comando sugerido:

```bash
npx firebase emulators:exec --config firebase/firebase.json --only auth,firestore "npm run test --workspace @aulaplan/api"
```

## E2E

Playwright debe cubrir solo el camino de mayor valor:

```text
login
→ teacher/subject/group demo
→ constraint
→ generate
→ review
→ publish
```

[Volver al índice](./README.md)

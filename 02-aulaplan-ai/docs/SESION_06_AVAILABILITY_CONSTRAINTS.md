# 06 — Disponibilidad y restricciones

**Duración:** 1 hora 30 minutos.

## Objetivo

Modelar reglas duras y blandas que después consumirá el scheduler.

## Distribución de tiempo

- **00–20 min** — Hard vs soft
- **20–40 min** — Availability
- **40–60 min** — Constraint schema
- **60–75 min** — CRUD
- **75–90 min** — Casos

## Conceptos

- hard constraints
- soft constraints
- weights
- scope
- parameters
- validation before persistence

## Desarrollo

### 1. Disponibilidad

Para cada profesor registrar disponibilidad por `timeBlockId` y una preferencia opcional.

### 2. Tipos de constraint

Definir un catálogo: `TEACHER_UNAVAILABLE`, `TEACHER_PREFERRED`, `ROOM_REQUIRED`, `MAX_CONSECUTIVE`, `MAX_DAILY_BLOCKS`, `AVOID_GAPS`.

### 3. Hard/soft

`hard=true` invalida una solución; `hard=false` afecta score mediante `weight`.

### 4. Parameters

Validar el contenido de `parameters` según `type`; no aceptar objetos arbitrarios sin schema.

### 5. Casos de prueba

Agregar ejemplos que puedan ser imposibles para preparar la siguiente fase de diagnóstico.

## Endpoints al cierre

- `GET/PUT /api/teachers/:teacherId/availability`
- `GET/POST/PUT/DELETE /api/constraints`

## Checklist de cierre

- [ ] Reglas duras diferenciadas
- [ ] Weights para reglas blandas
- [ ] Parámetros validados
- [ ] Restricciones imposibles representables

## Commit sugerido

```bash
git add .
git commit -m "feat: implement availability and constraints"
```

## Schemas de restricciones

### `availability.schema.ts`

```ts
import { z } from 'zod'

export const availabilityRuleSchema = z.object({
  teacherId: z.string().min(1),
  academicPeriodId: z.string().min(1),
  timeBlockId: z.string().min(1),
  available: z.boolean(),
  preferenceWeight: z.number().int().min(-100).max(100).default(0)
})
```

### `constraint.schema.ts`

```ts
import { z } from 'zod'

export const constraintTypeSchema = z.enum([
  'TEACHER_UNAVAILABLE',
  'TEACHER_PREFERRED',
  'ROOM_REQUIRED',
  'MAX_CONSECUTIVE',
  'MAX_DAILY_BLOCKS',
  'AVOID_GAPS'
])

export const constraintSchema = z.object({
  academicPeriodId: z.string().min(1),
  type: constraintTypeSchema,
  scope: z.enum(['GLOBAL', 'TEACHER', 'GROUP', 'SUBJECT', 'ROOM']),
  targetId: z.string().nullable().default(null),
  hard: z.boolean(),
  weight: z.number().int().min(0).max(100).default(10),
  parameters: z.record(z.string(), z.unknown()).default({}),
  active: z.boolean().default(true)
})
```

## Validación semántica

Después de Zod, agregar una función por tipo. Ejemplo:

```ts
import { AppError } from '../../core/errors'

export function validateConstraint(input: {
  type: string
  targetId: string | null
  parameters: Record<string, unknown>
}) {
  if (input.type === 'MAX_CONSECUTIVE') {
    const value = input.parameters.maxBlocks

    if (!Number.isInteger(value) || Number(value) < 1) {
      throw new AppError(
        422,
        'INVALID_CONSTRAINT_PARAMETERS',
        'MAX_CONSECUTIVE requires a positive integer maxBlocks'
      )
    }
  }

  if (input.type.startsWith('TEACHER_') && !input.targetId) {
    throw new AppError(
      422,
      'INVALID_CONSTRAINT_TARGET',
      'Teacher constraints require targetId'
    )
  }
}
```

Esto evita convertir `parameters` en una bolsa de datos sin contrato.

[Volver al índice](./README.md)

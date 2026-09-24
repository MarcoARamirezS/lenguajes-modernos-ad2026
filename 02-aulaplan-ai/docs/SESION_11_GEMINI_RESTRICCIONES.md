# 11 — Gemini: restricciones desde lenguaje natural

**Duración:** 1 hora 30 minutos.

## Objetivo

Integrar Gemini como parser asistido de restricciones, con salida estructurada, validación Zod y confirmación humana.

## Distribución de tiempo

- **00–20 min** — Responsabilidad de IA
- **20–40 min** — SDK
- **40–60 min** — Structured output
- **60–75 min** — Validation
- **75–90 min** — Safety/fallback

## Conceptos

- LLM as parser
- structured output
- schema validation
- human in the loop
- fallback

## Desarrollo

### 1. Instalar SDK

```bash
npm install --workspace apps/api @google/genai
```

### 2. Secret

Configurar `GEMINI_API_KEY` únicamente en backend/Netlify. No usar una variable `NUXT_PUBLIC_*`.

### 3. Prompt contract

Enviar tipos permitidos de restricción y pedir una estructura estricta. No pedir a Gemini que genere el horario final.

### 4. Validar

La respuesta pasa por Zod. Si el modelo devuelve profesor, grupo o salón inexistente, responder con una propuesta no aplicable y pedir corrección/confirmación.

### 5. Fallback

Si Gemini no está configurado, la aplicación debe seguir funcionando con captura manual de restricciones.

## Endpoints al cierre

- `POST /api/ai/constraints/parse`

## Checklist de cierre

- [ ] API key no llega al browser
- [ ] Salida inválida se rechaza
- [ ] Entidades inexistentes se detectan
- [ ] Usuario confirma antes de persistir
- [ ] Scheduler sigue siendo determinista

## Commit sugerido

```bash
git add .
git commit -m "feat: integrate Gemini constraint parser"
```

## Servicio Gemini

Mantener el modelo configurable porque los modelos disponibles y cuotas pueden cambiar.

### `apps/api/src/ai/constraint-parser.ts`

```ts
import { GoogleGenAI } from '@google/genai'
import { z } from 'zod'
import { AppError } from '../core/errors'

const parsedConstraintSchema = z.object({
  constraints: z.array(z.object({
    type: z.enum([
      'TEACHER_UNAVAILABLE',
      'TEACHER_PREFERRED',
      'ROOM_REQUIRED',
      'MAX_CONSECUTIVE',
      'MAX_DAILY_BLOCKS',
      'AVOID_GAPS'
    ]),
    targetName: z.string().nullable(),
    hard: z.boolean(),
    weight: z.number().int().min(0).max(100),
    parameters: z.record(z.string(), z.unknown())
  }))
})

const responseSchema = {
  type: 'object',
  properties: {
    constraints: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          type: {
            type: 'string',
            enum: [
              'TEACHER_UNAVAILABLE',
              'TEACHER_PREFERRED',
              'ROOM_REQUIRED',
              'MAX_CONSECUTIVE',
              'MAX_DAILY_BLOCKS',
              'AVOID_GAPS'
            ]
          },
          targetName: { type: ['string', 'null'] },
          hard: { type: 'boolean' },
          weight: { type: 'integer' },
          parameters: { type: 'object' }
        },
        required: ['type', 'targetName', 'hard', 'weight', 'parameters']
      }
    }
  },
  required: ['constraints']
}

export async function parseConstraintsWithAI(text: string) {
  const apiKey = process.env.GEMINI_API_KEY
  const model = process.env.GEMINI_MODEL

  if (!apiKey || !model) {
    throw new AppError(503, 'AI_NOT_CONFIGURED', 'Gemini is not configured')
  }

  const client = new GoogleGenAI({ apiKey })

  const interaction = await client.interactions.create({
    model,
    input: [
      'Convert the following academic scheduling instruction into constraints.',
      'Do not invent teachers, rooms or groups.',
      'Return only data matching the supplied JSON schema.',
      text
    ].join('\n'),
    response_format: {
      type: 'text',
      mime_type: 'application/json',
      schema: responseSchema
    }
  })

  if (!interaction.output_text) {
    throw new AppError(502, 'AI_EMPTY_RESPONSE', 'Gemini returned an empty response')
  }

  return parsedConstraintSchema.parse(JSON.parse(interaction.output_text))
}
```

## Endpoint

```ts
router.post('/ai/constraints/parse', async req => {
  const user = await requireAuth(req)
  requireRole(user, ['ADMIN', 'COORDINATOR'])

  const body = z.object({
    text: z.string().trim().min(5).max(2000)
  }).parse(await readJson(req))

  return json(await parseConstraintsWithAI(body.text))
})
```

## Validación contra datos reales

El `targetName` devuelto por IA debe resolverse contra profesores/grupos/salones existentes. Si hay cero o múltiples coincidencias, devolver `requiresConfirmation: true` en lugar de crear la restricción automáticamente.

[Volver al índice](./README.md)

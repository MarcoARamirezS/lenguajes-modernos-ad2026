# 04 — Academic Core: periodos, profesores y materias

**Duración:** 1 hora 30 minutos.

## Objetivo

Implementar los primeros módulos reales usando schema → service → repository → Firestore.

## Distribución de tiempo

- **00–15 min** — Modelo académico
- **15–35 min** — Schemas
- **35–60 min** — Repositories
- **60–75 min** — Services
- **75–90 min** — API tests

## Conceptos

- CRUD serverless
- DTO/schema
- business rules
- Firestore repository
- timestamps

## Desarrollo

### 1. Academic periods

Implementar creación, listado, consulta y actualización. Solo un periodo puede estar `ACTIVE` si esa regla se adopta en la institución.

### 2. Teachers

Campos mínimos: código, nombre, email, activo, máximo diario y máximo semanal.

### 3. Subjects

Campos mínimos: código, nombre, bloques semanales, tipo de salón requerido y estado.

### 4. Router

Registrar las rutas del contrato API. El router delega y no contiene reglas de negocio.

### 5. Pruebas

Cubrir creación válida, duplicado por código, recurso inexistente y actualización inválida.

## Endpoints al cierre

- `/api/academic-periods`
- `/api/teachers`
- `/api/subjects`

## Checklist de cierre

- [ ] CRUD básico funcional
- [ ] Códigos duplicados controlados
- [ ] Schemas compartidos donde convenga
- [ ] Datos persistidos en emulador

## Commit sugerido

```bash
git add .
git commit -m "feat: implement academic core"
```

## Implementación de referencia: Teachers

El patrón de Teachers se reutiliza en Periods y Subjects.

### `apps/api/src/modules/teachers/teacher.schema.ts`

```ts
import { z } from 'zod'

export const createTeacherSchema = z.object({
  code: z.string().trim().min(2).max(20).transform(v => v.toUpperCase()),
  name: z.string().trim().min(3).max(120),
  email: z.string().email(),
  active: z.boolean().default(true),
  maxDailyBlocks: z.number().int().positive().max(12).default(6),
  maxWeeklyBlocks: z.number().int().positive().max(60).default(30)
})

export const updateTeacherSchema = createTeacherSchema.partial()

export type CreateTeacherInput = z.infer<typeof createTeacherSchema>
export type Teacher = CreateTeacherInput & {
  id: string
  createdAt?: string
  updatedAt?: string
}
```

### `teacher.repository.ts`

```ts
import { firestoreRepository } from '../../repositories/firestore.repository'
import type { CreateTeacherInput } from './teacher.schema'

export const teacherRepository = firestoreRepository<CreateTeacherInput>('teachers')
```

### `teacher.service.ts`

```ts
import { AppError } from '../../core/errors'
import { db } from '../../firebase/admin'
import { teacherRepository } from './teacher.repository'
import type { CreateTeacherInput } from './teacher.schema'

async function assertCodeAvailable(code: string, ignoreId?: string) {
  const snapshot = await db.collection('teachers')
    .where('code', '==', code)
    .limit(2)
    .get()

  const duplicate = snapshot.docs.find(doc => doc.id !== ignoreId)

  if (duplicate) {
    throw new AppError(409, 'TEACHER_CODE_EXISTS', 'Teacher code already exists')
  }
}

export const teacherService = {
  list: () => teacherRepository.list(),
  getById: (id: string) => teacherRepository.getById(id),

  async create(input: CreateTeacherInput) {
    await assertCodeAvailable(input.code)
    return await teacherRepository.create(input)
  },

  async update(id: string, input: Partial<CreateTeacherInput>) {
    if (input.code) {
      await assertCodeAvailable(input.code, id)
    }
    return await teacherRepository.update(id, input)
  },

  remove: (id: string) => teacherRepository.remove(id)
}
```

### `teacher.routes.ts`

```ts
import type { Router } from '../../core/router'
import { json, noContent, readJson } from '../../core/http'
import { createTeacherSchema, updateTeacherSchema } from './teacher.schema'
import { teacherService } from './teacher.service'

export function registerTeacherRoutes(router: Router) {
  router.get('/teachers', async () => json(await teacherService.list()))

  router.get('/teachers/:id', async (_req, params) => {
    return json(await teacherService.getById(params.id))
  })

  router.post('/teachers', async req => {
    const input = createTeacherSchema.parse(await readJson(req))
    return json(await teacherService.create(input), 201)
  })

  router.put('/teachers/:id', async (req, params) => {
    const input = updateTeacherSchema.parse(await readJson(req))
    return json(await teacherService.update(params.id, input))
  })

  router.delete('/teachers/:id', async (_req, params) => {
    await teacherService.remove(params.id)
    return noContent()
  })
}
```

## Academic Period schema

```ts
import { z } from 'zod'

export const academicPeriodSchema = z.object({
  name: z.string().trim().min(3).max(80),
  startDate: z.string().date(),
  endDate: z.string().date(),
  status: z.enum(['DRAFT', 'ACTIVE', 'CLOSED']).default('DRAFT')
}).refine(value => value.endDate >= value.startDate, {
  message: 'endDate must be greater than or equal to startDate',
  path: ['endDate']
})
```

## Subject schema

```ts
import { z } from 'zod'

export const subjectSchema = z.object({
  code: z.string().trim().min(2).max(20).transform(v => v.toUpperCase()),
  name: z.string().trim().min(3).max(120),
  weeklyBlocks: z.number().int().positive().max(10),
  requiredRoomType: z.enum([
    'CLASSROOM',
    'LAB',
    'COMPUTER_LAB',
    'AUDITORIUM'
  ]).nullable().default(null),
  active: z.boolean().default(true)
})
```

Repetir la misma separación `schema/repository/service/routes` para `academic-periods` y `subjects`, y registrar las tres funciones de rutas desde `app.ts`.

[Volver al índice](./README.md)

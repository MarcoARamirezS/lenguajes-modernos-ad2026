# 05 — Grupos, salones, bloques y asignaciones

**Duración:** 1 hora 30 minutos.

## Objetivo

Completar los recursos que forman el espacio de búsqueda del generador de horarios.

## Distribución de tiempo

- **00–15 min** — Relaciones
- **15–35 min** — Groups/Rooms
- **35–55 min** — Time blocks
- **55–75 min** — Assignments
- **75–90 min** — Validación cruzada

## Conceptos

- document references by id
- capacity rules
- room types
- time block ordering
- teaching assignments

## Desarrollo

### 1. Groups

Agregar `studentCount` y `academicPeriodId`. Rechazar grupos sin periodo válido.

### 2. Rooms

Agregar `capacity`, `type`, `building` y `active`. Validar capacidad positiva.

### 3. Time blocks

Representar día, inicio, fin y orden. Evitar bloques duplicados dentro del mismo periodo.

### 4. Teaching assignments

Relacionar profesor, materia y grupo. Definir carga semanal y tipo preferido/requerido de salón.

### 5. Validación cruzada

Antes de crear una asignación comprobar que todas las referencias existen y pertenecen al periodo correcto.

## Endpoints al cierre

- `/api/groups`
- `/api/rooms`
- `/api/time-blocks`
- `/api/teaching-assignments`

## Checklist de cierre

- [ ] Capacidad validada
- [ ] Referencias inexistentes rechazadas
- [ ] Bloques ordenables
- [ ] Asignaciones listas para scheduling

## Commit sugerido

```bash
git add .
git commit -m "feat: implement academic resources"
```

## Schemas principales

### Groups

```ts
import { z } from 'zod'

export const groupSchema = z.object({
  code: z.string().trim().min(2).max(30).transform(v => v.toUpperCase()),
  name: z.string().trim().min(2).max(100),
  studentCount: z.number().int().positive().max(500),
  academicPeriodId: z.string().min(1),
  active: z.boolean().default(true)
})
```

### Rooms

```ts
import { z } from 'zod'

export const roomSchema = z.object({
  code: z.string().trim().min(2).max(30).transform(v => v.toUpperCase()),
  name: z.string().trim().min(2).max(100),
  capacity: z.number().int().positive().max(1000),
  type: z.enum(['CLASSROOM', 'LAB', 'COMPUTER_LAB', 'AUDITORIUM']),
  building: z.string().trim().min(1).max(100),
  active: z.boolean().default(true)
})
```

### Time blocks

```ts
import { z } from 'zod'

const hhmm = /^([01]\d|2[0-3]):[0-5]\d$/

export const timeBlockSchema = z.object({
  academicPeriodId: z.string().min(1),
  day: z.enum(['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']),
  startTime: z.string().regex(hhmm),
  endTime: z.string().regex(hhmm),
  order: z.number().int().nonnegative(),
  active: z.boolean().default(true)
}).refine(value => value.endTime > value.startTime, {
  message: 'endTime must be later than startTime',
  path: ['endTime']
})
```

### Teaching assignments

```ts
import { z } from 'zod'

export const teachingAssignmentSchema = z.object({
  academicPeriodId: z.string().min(1),
  teacherId: z.string().min(1),
  subjectId: z.string().min(1),
  groupId: z.string().min(1),
  weeklyBlocks: z.number().int().positive().max(10),
  preferredRoomType: z.enum([
    'CLASSROOM',
    'LAB',
    'COMPUTER_LAB',
    'AUDITORIUM'
  ]).nullable().default(null),
  active: z.boolean().default(true)
})
```

## Regla importante del service

Antes de crear `teachingAssignment`, cargar profesor, materia, grupo y periodo. Rechazar si cualquiera no existe, está inactivo o pertenece a un periodo incompatible. No dejar esta validación en el frontend.

[Volver al índice](./README.md)

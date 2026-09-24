# 08 — Scheduling Domain y validación previa

**Duración:** 1 hora 30 minutos.

## Objetivo

Transformar los documentos Firestore en un problema de asignación independiente de la persistencia.

## Distribución de tiempo

- **00–20 min** — Domain model
- **20–40 min** — Candidates
- **40–60 min** — Hard rules
- **60–75 min** — Input validator
- **75–90 min** — Fixtures

## Conceptos

- constraint satisfaction
- candidate slots
- immutable input
- preflight validation
- domain isolation

## Desarrollo

### 1. ScheduleProblem

Crear un objeto de dominio con assignments, teachers, groups, rooms, timeBlocks, availability y constraints.

### 2. Candidate

Un candidato representa `assignment + room + timeBlock`. Generarlo solo si cumple filtros estáticos como capacidad y tipo de salón.

### 3. Hard rule functions

Crear funciones pequeñas: teacher conflict, group conflict, room conflict, availability, capacity, room type.

### 4. Preflight

Detectar antes del solver datos incompletos: asignación sin candidatos, profesor sin disponibilidad, materia sin carga, grupo sin tamaño.

### 5. Fixtures

Crear datasets pequeños y deterministas para pruebas: viable, conflicto simple e imposible.

## Endpoints al cierre

- `POST /api/schedules/validate-input`

## Checklist de cierre

- [ ] Dominio no importa Firebase
- [ ] Hard rules tienen unit tests
- [ ] Caso imposible se detecta temprano cuando sea posible
- [ ] Fixtures reproducibles

## Commit sugerido

```bash
git add .
git commit -m "feat: model scheduling domain"
```

## Tipos del dominio

### `apps/api/src/scheduler/types.ts`

```ts
export type RoomType = 'CLASSROOM' | 'LAB' | 'COMPUTER_LAB' | 'AUDITORIUM'

export type Teacher = {
  id: string
  maxDailyBlocks: number
  maxWeeklyBlocks: number
}

export type Group = {
  id: string
  studentCount: number
}

export type Room = {
  id: string
  capacity: number
  type: RoomType
  active: boolean
}

export type TimeBlock = {
  id: string
  day: string
  order: number
}

export type TeachingAssignment = {
  id: string
  teacherId: string
  subjectId: string
  groupId: string
  weeklyBlocks: number
  requiredRoomType: RoomType | null
}

export type AvailabilityRule = {
  teacherId: string
  timeBlockId: string
  available: boolean
  preferenceWeight: number
}

export type ScheduleTask = {
  id: string
  assignmentId: string
  teacherId: string
  subjectId: string
  groupId: string
  requiredRoomType: RoomType | null
}

export type Candidate = {
  taskId: string
  assignmentId: string
  teacherId: string
  subjectId: string
  groupId: string
  roomId: string
  timeBlockId: string
}

export type ScheduleEntry = Candidate

export type ScheduleProblem = {
  teachers: Teacher[]
  groups: Group[]
  rooms: Room[]
  timeBlocks: TimeBlock[]
  assignments: TeachingAssignment[]
  availability: AvailabilityRule[]
}
```

### `apps/api/src/scheduler/problem.ts`

```ts
import type {
  Candidate,
  ScheduleProblem,
  ScheduleTask
} from './types'

export function buildTasks(problem: ScheduleProblem): ScheduleTask[] {
  return problem.assignments.flatMap(assignment => {
    return Array.from({ length: assignment.weeklyBlocks }, (_, index) => ({
      id: `${assignment.id}:${index + 1}`,
      assignmentId: assignment.id,
      teacherId: assignment.teacherId,
      subjectId: assignment.subjectId,
      groupId: assignment.groupId,
      requiredRoomType: assignment.requiredRoomType
    }))
  })
}

export function buildCandidates(
  problem: ScheduleProblem,
  task: ScheduleTask
): Candidate[] {
  const group = problem.groups.find(item => item.id === task.groupId)

  if (!group) {
    return []
  }

  const blocked = new Set(
    problem.availability
      .filter(rule => rule.teacherId === task.teacherId && !rule.available)
      .map(rule => rule.timeBlockId)
  )

  return problem.timeBlocks.flatMap(timeBlock => {
    if (blocked.has(timeBlock.id)) {
      return []
    }

    return problem.rooms
      .filter(room => room.active)
      .filter(room => room.capacity >= group.studentCount)
      .filter(room => !task.requiredRoomType || room.type === task.requiredRoomType)
      .map(room => ({
        taskId: task.id,
        assignmentId: task.assignmentId,
        teacherId: task.teacherId,
        subjectId: task.subjectId,
        groupId: task.groupId,
        roomId: room.id,
        timeBlockId: timeBlock.id
      }))
  })
}
```

## Preflight

Antes de invocar el solver, construir todos los tasks y comprobar que cada uno tenga al menos un candidato. Si un task tiene cero candidatos, devolver un diagnóstico específico y no gastar tiempo de búsqueda.

[Volver al índice](./README.md)

# 09 — Scheduler I: Backtracking

**Duración:** 1 hora 30 minutos.

## Objetivo

Construir el primer motor capaz de encontrar un horario válido sin depender de IA ni de una librería de optimización.

## Distribución de tiempo

- **00–20 min** — Backtracking
- **20–40 min** — State
- **40–65 min** — Recursive search
- **65–80 min** — Time budget
- **80–90 min** — Tests

## Conceptos

- depth-first search
- backtracking
- state mutation/rollback
- time budget
- deterministic seed

## Desarrollo

### 1. Estado

Mantener ocupación por profesor, grupo y salón. Cada asignación debe poder aplicarse y revertirse sin reconstruir todo el estado.

### 2. Selección

Elegir una asignación no colocada, probar candidatos y retroceder cuando ninguna opción sea válida.

### 3. Terminación

Solución completa cuando todas las sesiones requeridas fueron colocadas.

### 4. Presupuesto

Agregar `deadline` y detener búsqueda al llegar a `MAX_SOLVER_MS`. El proyecto académico debe usar datasets que terminen holgadamente dentro del runtime serverless.

### 5. Determinismo

Aceptar `seed` para poder repetir pruebas y comparar mejoras.

## Endpoints al cierre

- `POST /api/schedules/generate`

## Checklist de cierre

- [ ] Dataset mínimo genera horario
- [ ] No hay conflictos duros
- [ ] Caso imposible devuelve diagnóstico
- [ ] Búsqueda respeta time budget

## Commit sugerido

```bash
git add .
git commit -m "feat: implement backtracking scheduler"
```

## Implementación base del solver

### `apps/api/src/scheduler/solver.ts`

```ts
import { buildCandidates, buildTasks } from './problem'
import type {
  Candidate,
  ScheduleEntry,
  ScheduleProblem,
  ScheduleTask
} from './types'

type SolverOptions = {
  maxSolverMs: number
}

type SolverResult = {
  solved: boolean
  entries: ScheduleEntry[]
  elapsedMs: number
  nodes: number
  timedOut: boolean
}

type State = {
  teacherBusy: Set<string>
  groupBusy: Set<string>
  roomBusy: Set<string>
  entries: ScheduleEntry[]
}

function key(resourceId: string, timeBlockId: string) {
  return `${resourceId}:${timeBlockId}`
}

function canPlace(state: State, candidate: Candidate) {
  return !state.teacherBusy.has(key(candidate.teacherId, candidate.timeBlockId)) &&
    !state.groupBusy.has(key(candidate.groupId, candidate.timeBlockId)) &&
    !state.roomBusy.has(key(candidate.roomId, candidate.timeBlockId))
}

function apply(state: State, candidate: Candidate) {
  state.teacherBusy.add(key(candidate.teacherId, candidate.timeBlockId))
  state.groupBusy.add(key(candidate.groupId, candidate.timeBlockId))
  state.roomBusy.add(key(candidate.roomId, candidate.timeBlockId))
  state.entries.push(candidate)
}

function rollback(state: State, candidate: Candidate) {
  state.entries.pop()
  state.teacherBusy.delete(key(candidate.teacherId, candidate.timeBlockId))
  state.groupBusy.delete(key(candidate.groupId, candidate.timeBlockId))
  state.roomBusy.delete(key(candidate.roomId, candidate.timeBlockId))
}

export function solveSchedule(
  problem: ScheduleProblem,
  options: SolverOptions
): SolverResult {
  const startedAt = Date.now()
  const deadline = startedAt + options.maxSolverMs
  let nodes = 0
  let timedOut = false

  const tasks = buildTasks(problem)
  const candidates = new Map<string, Candidate[]>()

  for (const task of tasks) {
    const values = buildCandidates(problem, task)

    if (values.length === 0) {
      return {
        solved: false,
        entries: [],
        elapsedMs: Date.now() - startedAt,
        nodes,
        timedOut: false
      }
    }

    candidates.set(task.id, values)
  }

  const orderedTasks = [...tasks].sort((a, b) => {
    return (candidates.get(a.id)?.length ?? 0) -
      (candidates.get(b.id)?.length ?? 0)
  })

  const state: State = {
    teacherBusy: new Set(),
    groupBusy: new Set(),
    roomBusy: new Set(),
    entries: []
  }

  function search(index: number): boolean {
    if (Date.now() >= deadline) {
      timedOut = true
      return false
    }

    if (index === orderedTasks.length) {
      return true
    }

    nodes += 1

    const task: ScheduleTask = orderedTasks[index]
    const values = candidates.get(task.id) ?? []

    for (const candidate of values) {
      if (!canPlace(state, candidate)) {
        continue
      }

      apply(state, candidate)

      if (search(index + 1)) {
        return true
      }

      rollback(state, candidate)
    }

    return false
  }

  const solved = search(0)

  return {
    solved,
    entries: solved ? [...state.entries] : [],
    elapsedMs: Date.now() - startedAt,
    nodes,
    timedOut
  }
}
```

## Regla de diseño

Esta primera versión busca **una solución válida**, no la mejor. La siguiente sesión transformará la búsqueda para mantener `best-so-far` y calcular score.

[Volver al índice](./README.md)

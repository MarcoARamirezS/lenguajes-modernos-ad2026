# 10 — Scheduler II: heurísticas y scoring

**Duración:** 1 hora 30 minutos.

## Objetivo

Mejorar rendimiento y calidad con ordenamiento inteligente de variables/candidatos y una función explícita de score.

## Distribución de tiempo

- **00–20 min** — MRV / most constrained
- **20–40 min** — Candidate ordering
- **40–60 min** — Scoring
- **60–75 min** — Best-so-far
- **75–90 min** — Benchmark

## Conceptos

- MRV heuristic
- least constraining value
- soft constraints
- score
- best-so-far search

## Desarrollo

### 1. Heurística de variable

Elegir primero la asignación con menos candidatos disponibles. Esto reduce ramas imposibles tempranamente.

### 2. Orden de candidatos

Probar primero horarios preferidos, salas de ajuste exacto y opciones que no creen huecos.

### 3. Score

Definir puntuaciones explícitas y documentadas. Ejemplo: preferencia cumplida +10, hueco largo -15, última hora -5.

### 4. Best solution

Guardar la mejor solución completa encontrada. Si el deadline llega, devolver la mejor válida, no una parcial silenciosa.

### 5. Benchmark

Comparar nodos explorados y tiempo del backtracking básico vs heurístico usando el mismo fixture y seed.

## Endpoints al cierre

- `POST /api/schedules/generate`

## Checklist de cierre

- [ ] Score reproducible
- [ ] Hard violations siempre 0
- [ ] Heurística explora menos nodos en fixture
- [ ] Respuesta incluye métricas de solver

## Commit sugerido

```bash
git add .
git commit -m "feat: optimize scheduler with heuristics and scoring"
```

## Scoring

### `apps/api/src/scheduler/scoring.ts`

```ts
import type { ScheduleEntry, ScheduleProblem } from './types'

export function scoreSchedule(
  problem: ScheduleProblem,
  entries: ScheduleEntry[]
) {
  let score = 1000
  let softViolations = 0

  const blockById = new Map(problem.timeBlocks.map(block => [block.id, block]))

  for (const entry of entries) {
    const preference = problem.availability.find(rule =>
      rule.teacherId === entry.teacherId &&
      rule.timeBlockId === entry.timeBlockId
    )

    if (preference?.preferenceWeight) {
      score += preference.preferenceWeight
    }
  }

  const byTeacherDay = new Map<string, number[]>()

  for (const entry of entries) {
    const block = blockById.get(entry.timeBlockId)
    if (!block) continue

    const key = `${entry.teacherId}:${block.day}`
    const orders = byTeacherDay.get(key) ?? []
    orders.push(block.order)
    byTeacherDay.set(key, orders)
  }

  for (const orders of byTeacherDay.values()) {
    orders.sort((a, b) => a - b)

    for (let i = 1; i < orders.length; i += 1) {
      const gap = orders[i] - orders[i - 1]
      if (gap > 1) {
        score -= (gap - 1) * 10
        softViolations += 1
      }
    }
  }

  return { score, softViolations }
}
```

## Mejora del search

En lugar de detenerse en la primera solución completa:

1. calcular score;
2. comparar con `bestScore`;
3. clonar entries si mejora;
4. continuar mientras exista tiempo;
5. al llegar al deadline devolver la mejor solución válida encontrada.

Pseudoestructura:

```ts
let bestEntries: ScheduleEntry[] = []
let bestScore = Number.NEGATIVE_INFINITY

function search(index: number) {
  if (Date.now() >= deadline) return

  if (index === orderedTasks.length) {
    const result = scoreSchedule(problem, state.entries)

    if (result.score > bestScore) {
      bestScore = result.score
      bestEntries = structuredClone(state.entries)
    }

    return
  }

  // explorar candidatos y rollback
}
```

## Métricas de respuesta

El endpoint de generación debe devolver como mínimo:

```json
{
  "solved": true,
  "score": 920,
  "softViolations": 3,
  "nodes": 1842,
  "elapsedMs": 642,
  "timedOut": false
}
```

[Volver al índice](./README.md)

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 11](./SESION_11_BACKTRACKING_SOLVER.md) · [Sesión 13 →](./SESION_13_GEMINI_AI.md)

# Sesión 12 — Heurísticas y scoring

**Duración:** 1 h 30 min  
**Objetivo:** pasar de “una solución válida” a “la mejor solución encontrada”.

## Distribución

```text
00–15  Función objetivo
15–35  preferencias
35–55  penalizaciones
55–70  gaps
70–82  comparación de soluciones
82–90  commit
```

## 1. Scoring

### `apps/api/src/scheduler/scoring.py`

```python
from collections import defaultdict
from src.scheduler.domain import Candidate, SchedulerContext


def score_solution(assignments: list[Candidate], context: SchedulerContext) -> int:
    score = 0
    preference = {(x.teacher_id, x.time_block_id): x.preference_weight for x in context.availability}

    for candidate in assignments:
        score += preference.get((candidate.teacher_id, candidate.time_block_id), 0)
        for constraint in context.constraints:
            if constraint.priority != "SOFT":
                continue
            if constraint.type == "TEACHER_PREFERRED" and constraint.target_id == candidate.teacher_id:
                if constraint.params.get("time_block_id") == candidate.time_block_id:
                    score += constraint.weight
            if constraint.type == "GROUP_AVOID_LAST_BLOCK" and constraint.target_id == candidate.group_id:
                block = context.time_blocks[candidate.time_block_id]
                if block.order >= int(constraint.params.get("from_order", 6)):
                    score -= abs(constraint.weight)

    score -= _teacher_gap_penalty(assignments, context)
    return score


def _teacher_gap_penalty(assignments: list[Candidate], context: SchedulerContext) -> int:
    by_teacher_day: dict[tuple[str, str], list[int]] = defaultdict(list)
    for candidate in assignments:
        block = context.time_blocks[candidate.time_block_id]
        by_teacher_day[(candidate.teacher_id, block.day)].append(block.order)

    penalty = 0
    for orders in by_teacher_day.values():
        ordered = sorted(orders)
        for left, right in zip(ordered, ordered[1:]):
            if right - left > 1:
                penalty += (right - left - 1) * 3
    return penalty
```


## 2. Interpretación

Ejemplos:

```text
+10  bloque preferido
+15  TEACHER_PREFERRED
-3   por cada bloque vacío dentro de la jornada
-20  última hora si hay restricción blanda
```

El valor absoluto no significa nada por sí mismo. Lo importante es comparar soluciones generadas con las mismas reglas.

## 3. Integración

El solver de la sesión anterior ya llama:

```python
score = score_solution(state.assignments, context)
```

y conserva la solución con mayor score.

## 4. Ejercicio

Crea dos time blocks posibles para un profesor:

- `MON-01` preference_weight = 10
- `MON-05` preference_weight = 0

Ejecuta el solver y observa qué combinación obtiene mayor score.

## 5. Diagnóstico

Si no hay solución:

```json
{
  "status": "NO_SOLUTION",
  "score": null,
  "assignments": [],
  "issues": ["SEARCH_EXHAUSTED"]
}
```

Si una unidad ni siquiera tiene candidatos:

```text
NO_CANDIDATES:offering-id:sequence
```

## Checklist

- [ ] función de score pura.
- [ ] preferencias positivas.
- [ ] penalización de gaps.
- [ ] solver guarda mejor score.
- [ ] NO_SOLUTION distinguible.

## Commit

```bash
git add .
git commit -m "feat: optimize schedules with heuristics and scoring"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 11](./SESION_11_BACKTRACKING_SOLVER.md) · [Sesión 13 →](./SESION_13_GEMINI_AI.md)

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 10](./SESION_10_CANDIDATES_HARD_CONSTRAINTS.md) · [Sesión 12 →](./SESION_12_HEURISTICS_SCORING.md)

# Sesión 11 — Backtracking Solver

**Duración:** 1 h 30 min  
**Objetivo:** encontrar la primera solución válida respetando ocupación, cargas y distribución.

## Distribución

```text
00–15  Recursión y backtracking
15–35  ScheduleState
35–60  solver
60–75  MRV
75–85  tests
85–90  commit
```

## 1. Estado mutable controlado

### `apps/api/src/scheduler/state.py`

```python
from collections import defaultdict

from src.scheduler.domain import Candidate, SchedulerContext


class ScheduleState:
    def __init__(self, context: SchedulerContext) -> None:
        self.context = context
        self.assignments: list[Candidate] = []
        self.teacher_slots: set[tuple[str, str]] = set()
        self.group_slots: set[tuple[str, str]] = set()
        self.room_slots: set[tuple[str, str]] = set()
        self.teacher_daily: dict[tuple[str, str], int] = defaultdict(int)
        self.teacher_weekly: dict[str, int] = defaultdict(int)
        self.offering_days: dict[str, set[str]] = defaultdict(set)

    def can_place(self, candidate: Candidate) -> bool:
        block = self.context.time_blocks[candidate.time_block_id]
        teacher = self.context.teachers[candidate.teacher_id]
        slot = candidate.time_block_id

        if (candidate.teacher_id, slot) in self.teacher_slots:
            return False
        if (candidate.group_id, slot) in self.group_slots:
            return False
        if (candidate.room_id, slot) in self.room_slots:
            return False
        if self.teacher_daily[(candidate.teacher_id, block.day)] >= teacher.max_daily_blocks:
            return False
        if self.teacher_weekly[candidate.teacher_id] >= teacher.max_weekly_blocks:
            return False
        if block.day in self.offering_days[candidate.offering_id]:
            return False
        return True

    def place(self, candidate: Candidate) -> None:
        block = self.context.time_blocks[candidate.time_block_id]
        self.assignments.append(candidate)
        self.teacher_slots.add((candidate.teacher_id, candidate.time_block_id))
        self.group_slots.add((candidate.group_id, candidate.time_block_id))
        self.room_slots.add((candidate.room_id, candidate.time_block_id))
        self.teacher_daily[(candidate.teacher_id, block.day)] += 1
        self.teacher_weekly[candidate.teacher_id] += 1
        self.offering_days[candidate.offering_id].add(block.day)

    def remove(self, candidate: Candidate) -> None:
        block = self.context.time_blocks[candidate.time_block_id]
        self.assignments.pop()
        self.teacher_slots.remove((candidate.teacher_id, candidate.time_block_id))
        self.group_slots.remove((candidate.group_id, candidate.time_block_id))
        self.room_slots.remove((candidate.room_id, candidate.time_block_id))
        self.teacher_daily[(candidate.teacher_id, block.day)] -= 1
        self.teacher_weekly[candidate.teacher_id] -= 1
        self.offering_days[candidate.offering_id].remove(block.day)
```


`ScheduleState` centraliza ocupaciones para no recalcular toda la solución en cada nodo.

## 2. Solver

### `apps/api/src/scheduler/solver.py`

```python
from dataclasses import dataclass

from src.scheduler.candidates import build_candidates, expand_units
from src.scheduler.domain import Candidate, SchedulerContext
from src.scheduler.scoring import score_solution
from src.scheduler.state import ScheduleState


@dataclass
class SolverResult:
    status: str
    score: int | None
    assignments: list[Candidate]
    nodes_visited: int
    issues: list[str]


def solve_schedule(context: SchedulerContext, max_nodes: int = 50000) -> SolverResult:
    units = expand_units(context)
    candidate_map = {unit.id: build_candidates(unit, context) for unit in units}

    empty = [unit.id for unit in units if not candidate_map[unit.id]]
    if empty:
        return SolverResult("NO_SOLUTION", None, [], 0, [f"NO_CANDIDATES:{item}" for item in empty])

    units.sort(key=lambda unit: len(candidate_map[unit.id]))
    state = ScheduleState(context)
    best_assignments: list[Candidate] = []
    best_score: int | None = None
    nodes = 0

    def search(index: int) -> None:
        nonlocal best_assignments, best_score, nodes
        if nodes >= max_nodes:
            return
        if index == len(units):
            score = score_solution(state.assignments, context)
            if best_score is None or score > best_score:
                best_score = score
                best_assignments = list(state.assignments)
            return

        unit = units[index]
        for candidate in candidate_map[unit.id]:
            nodes += 1
            if nodes >= max_nodes:
                return
            if not state.can_place(candidate):
                continue
            state.place(candidate)
            search(index + 1)
            state.remove(candidate)

    search(0)

    if not best_assignments:
        return SolverResult("NO_SOLUTION", None, [], nodes, ["SEARCH_EXHAUSTED"])

    return SolverResult("SOLVED", best_score, best_assignments, nodes, [])
```


## 3. Heurística MRV

Esta línea es muy importante:

```python
units.sort(key=lambda unit: len(candidate_map[unit.id]))
```

Se asignan primero las unidades con menos candidatos. Esto suele detectar conflictos antes y reduce el árbol de búsqueda.

## 4. Prueba unitaria

### `apps/api/tests/test_scheduler.py`

```python
from src.scheduler.domain import Group, Offering, Room, SchedulerContext, Subject, Teacher, TimeBlock
from src.scheduler.solver import solve_schedule


def build_context() -> SchedulerContext:
    return SchedulerContext(
        teachers={"t1": Teacher("t1", "Ana", 4, 10)},
        subjects={"s1": Subject("s1", "Programación", 2, "CLASSROOM")},
        groups={"g1": Group("g1", "A", 20)},
        rooms={"r1": Room("r1", "Aula 1", 30, "CLASSROOM")},
        time_blocks={
            "b1": TimeBlock("b1", "MONDAY", "08:00", "09:30", 1),
            "b2": TimeBlock("b2", "TUESDAY", "08:00", "09:30", 1),
        },
        offerings={"o1": Offering("o1", "s1", "g1", "t1", "p1")},
        availability=[],
        constraints=[],
    )


def test_solver_finds_valid_solution():
    result = solve_schedule(build_context(), max_nodes=1000)
    assert result.status == "SOLVED"
    assert len(result.assignments) == 2
    days = {build_context().time_blocks[x.time_block_id].day for x in result.assignments}
    assert len(days) == 2
```


## 5. Ejecutar

macOS/Linux:

```bash
cd apps/api
source .venv/bin/activate
PYTHONPATH=. pytest tests/test_scheduler.py -q
```

Windows:

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH="."
pytest tests/test_scheduler.py -q
```

## Resultado esperado

```text
1 passed
```

## Qué hace backtracking

```text
tomar unidad
  ↓
probar candidato
  ↓
can_place?
 ├── no → siguiente candidato
 └── sí
      ↓
    place
      ↓
    recurse
      ↓
    remove
```

## Errores frecuentes

- Mutar el contexto en vez del estado.
- No hacer `remove()` al regresar.
- Permitir dos sesiones de la misma offering el mismo día sin intención.
- Buscar sin límite de nodos.

## Checklist

- [ ] state controla ocupaciones.
- [ ] backtracking recursivo.
- [ ] MRV activo.
- [ ] límite `max_nodes`.
- [ ] test verde.

## Commit

```bash
git add .
git commit -m "feat: implement schedule backtracking solver"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 10](./SESION_10_CANDIDATES_HARD_CONSTRAINTS.md) · [Sesión 12 →](./SESION_12_HEURISTICS_SCORING.md)

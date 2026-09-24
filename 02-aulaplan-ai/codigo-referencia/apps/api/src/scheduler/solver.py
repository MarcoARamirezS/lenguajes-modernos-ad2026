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

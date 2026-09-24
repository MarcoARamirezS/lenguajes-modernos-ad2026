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

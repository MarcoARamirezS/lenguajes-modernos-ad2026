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

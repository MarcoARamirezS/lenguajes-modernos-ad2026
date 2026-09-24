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

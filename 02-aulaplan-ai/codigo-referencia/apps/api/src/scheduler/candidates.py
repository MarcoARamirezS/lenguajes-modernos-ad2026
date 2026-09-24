from src.scheduler.domain import AssignmentUnit, Candidate, SchedulerContext


def expand_units(context: SchedulerContext) -> list[AssignmentUnit]:
    units: list[AssignmentUnit] = []
    for offering in context.offerings.values():
        subject = context.subjects[offering.subject_id]
        for sequence in range(1, subject.weekly_blocks + 1):
            units.append(AssignmentUnit(f"{offering.id}:{sequence}", offering.id, sequence))
    return units


def build_candidates(unit: AssignmentUnit, context: SchedulerContext) -> list[Candidate]:
    offering = context.offerings[unit.offering_id]
    subject = context.subjects[offering.subject_id]
    group = context.groups[offering.group_id]

    unavailable = {
        item.time_block_id
        for item in context.availability
        if item.teacher_id == offering.teacher_id and not item.available
    }

    candidates: list[Candidate] = []
    for block in context.time_blocks.values():
        if block.id in unavailable:
            continue
        if _blocked_by_hard_constraint(offering.teacher_id, offering.group_id, block.id, context):
            continue

        for room in context.rooms.values():
            if room.capacity < group.student_count:
                continue
            if subject.required_room_type and room.type != subject.required_room_type:
                continue
            candidates.append(Candidate(
                unit_id=unit.id,
                offering_id=offering.id,
                teacher_id=offering.teacher_id,
                group_id=offering.group_id,
                subject_id=offering.subject_id,
                room_id=room.id,
                time_block_id=block.id,
            ))
    return candidates


def _blocked_by_hard_constraint(teacher_id: str, group_id: str, block_id: str, context: SchedulerContext) -> bool:
    for constraint in context.constraints:
        if constraint.priority != "HARD":
            continue
        if constraint.type == "TEACHER_UNAVAILABLE" and constraint.target_id == teacher_id and constraint.params.get("time_block_id") == block_id:
            return True
        if constraint.type == "GROUP_UNAVAILABLE" and constraint.target_id == group_id and constraint.params.get("time_block_id") == block_id:
            return True
    return False

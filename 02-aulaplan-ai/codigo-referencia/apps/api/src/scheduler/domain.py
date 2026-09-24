from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Teacher:
    id: str
    name: str
    max_daily_blocks: int
    max_weekly_blocks: int


@dataclass(frozen=True)
class Subject:
    id: str
    name: str
    weekly_blocks: int
    required_room_type: str


@dataclass(frozen=True)
class Group:
    id: str
    name: str
    student_count: int


@dataclass(frozen=True)
class Room:
    id: str
    name: str
    capacity: int
    type: str


@dataclass(frozen=True)
class TimeBlock:
    id: str
    day: str
    start_time: str
    end_time: str
    order: int


@dataclass(frozen=True)
class Offering:
    id: str
    subject_id: str
    group_id: str
    teacher_id: str
    academic_period_id: str


@dataclass(frozen=True)
class Availability:
    teacher_id: str
    time_block_id: str
    available: bool
    preference_weight: int = 0


@dataclass(frozen=True)
class Constraint:
    type: str
    priority: str
    target_type: str
    target_id: str
    weight: int
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssignmentUnit:
    id: str
    offering_id: str
    sequence: int


@dataclass(frozen=True)
class Candidate:
    unit_id: str
    offering_id: str
    teacher_id: str
    group_id: str
    subject_id: str
    room_id: str
    time_block_id: str


@dataclass(frozen=True)
class ScheduledClass:
    candidate: Candidate
    score: int = 0


@dataclass
class SchedulerContext:
    teachers: dict[str, Teacher]
    subjects: dict[str, Subject]
    groups: dict[str, Group]
    rooms: dict[str, Room]
    time_blocks: dict[str, TimeBlock]
    offerings: dict[str, Offering]
    availability: list[Availability]
    constraints: list[Constraint]

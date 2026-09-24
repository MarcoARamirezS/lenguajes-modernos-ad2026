from typing import Any, Literal
from pydantic import BaseModel, Field


class GenerateScheduleRequest(BaseModel):
    academic_period_id: str = Field(min_length=1)
    max_nodes: int = Field(default=50000, ge=100, le=500000)


class ParseConstraintRequest(BaseModel):
    text: str = Field(min_length=5, max_length=3000)


class ParsedConstraint(BaseModel):
    type: Literal[
        "TEACHER_UNAVAILABLE",
        "TEACHER_PREFERRED",
        "GROUP_UNAVAILABLE",
        "GROUP_AVOID_LAST_BLOCK",
        "MAX_CONSECUTIVE",
    ]
    priority: Literal["HARD", "SOFT"]
    target_type: Literal["TEACHER", "GROUP"]
    target: str
    weight: int = Field(default=0, ge=-1000, le=1000)
    params: dict[str, Any] = Field(default_factory=dict)


class ParsedConstraintBatch(BaseModel):
    constraints: list[ParsedConstraint]

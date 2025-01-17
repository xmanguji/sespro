from datetime import datetime
from typing import Optional
from pydantic.types import UUID4

from .base import BaseModel, BaseOutUuid


class ParsedAuditCreate(BaseModel):
    uuid: UUID4
    audit_template: UUID4
    premises: UUID4
    user: UUID4
    raw_data_key: str
    raw_data_uri: str
    score: Optional[int] = 0
    max_score: Optional[int] = 0
    score_precentage: Optional[float] = 0
    start_time: datetime
    end_time: datetime
    final_comments: Optional[str]
    extra: Optional[dict]
    date_submitted: Optional[datetime]
    timezone: Optional[str]


class ParsedAuditUpdate(BaseOutUuid):
    uuid: Optional[UUID4]
    audit_template: Optional[UUID4]
    premises: Optional[UUID4]
    user: Optional[UUID4]
    raw_data_key: Optional[str]
    raw_data_uri: Optional[str]
    score: Optional[int]
    max_score: Optional[int]
    score_percentage: Optional[float]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    date_submitted: Optional[datetime]
    timezone: Optional[str]


class ParsedQuestionCreate(BaseOutUuid):
    category: UUID4
    worth: int
    passed: bool
    notes: str


class ParsedQuestionUpdate(BaseOutUuid):
    category: Optional[UUID4]
    worth: Optional[int]
    passed: Optional[bool]
    notes: Optional[str]

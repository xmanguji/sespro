from datetime import datetime
from typing import Optional

from pydantic.types import UUID4

from .base import BaseModel, BaseOutUuid


class GenericReport(BaseModel):
    uuid: Optional[str]
    location_name: Optional[str]
    location_uuid: Optional[str]
    score: Optional[float]
    score_percentage: Optional[float]
    final_comments: Optional[str]
    parsed_question_uuid: Optional[str]
    question_text: Optional[str]
    question_uuid: Optional[str]
    category_text: Optional[str]
    category_uuid: Optional[str]
    worth: Optional[int]
    is_passed: Optional[str]
    answer_notes: Optional[str]
    date_submitted: Optional[datetime]


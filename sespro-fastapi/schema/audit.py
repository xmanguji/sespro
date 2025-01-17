from typing import List, Optional

from pydantic.types import UUID4, Json

from .base import BaseModel, BaseOut, BaseOutUuid


class AuditTemplate(BaseOut):
    categories: Json
    questions: Json


class AuditTemplateCreate(BaseModel):
    pass


class AuditTemplateUpdate(BaseModel):
    pass


class AuditTemplateName(BaseModel):
    uuid: str
    name: str

class QuestionText(BaseModel):
    text: str


class ListAuditTemplateName(BaseModel):
    audits: List[AuditTemplateName]


class QuestionCreate(BaseOutUuid):
    typed: int
    text: str
    worth: int
    weight: float
    attachment: Json


class QuestionUpdate(BaseOutUuid):
    typed: Optional[int]
    text: Optional[str]
    worth: Optional[int]
    weight: Optional[float]
    attachment: Optional[Json]


class AuditImageCreate(BaseModel):
    uuid: UUID4
    user: UUID4
    premises: UUID4
    question: UUID4
    parsed_question: Optional[UUID4]
    parsed_audit: Optional[UUID4]
    image_key: str
    image_uri: str

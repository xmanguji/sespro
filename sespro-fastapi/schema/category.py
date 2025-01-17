from typing import List, Optional, Any

from pony.orm.ormtypes import TrackedList
from pydantic.types import UUID4

from .base import BaseModel
from .audit import QuestionText


class CategoryCreate(BaseModel):
    text: str
    icon: str
    color: str
    parent: Optional[str]
    children: List[str]
    challenge: bool = False


class CategoryOut(CategoryCreate):
    id: int
    uuid: UUID4
    text: str
    icon: str
    color: str
    parent: Optional[str]
    children: List[str]
    challenge: bool = False


class CategoryUpdate(CategoryCreate):
    text: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    parent: Optional[str]
    children: Optional[List[str]]
    challenge: Optional[bool] = False


class ReadQuestion(BaseModel):
    uuid: Any
    text: str
    weight: int
    id: str


# class ReadCategories(BaseModel):
#     categories: List[ReadCategory]


class ReadCategory(BaseModel):
    uuid: str
    text: str
    id: str
    audit_id: str
    questions: List[ReadQuestion]



class ReadCategories(BaseModel):
    categories: List[ReadCategory]
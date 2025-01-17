from typing import Optional, Set, List
from uuid import UUID

from pydantic import EmailStr

from .base import BaseModel, BaseOut, BaseOutName
from .templates import ReadTemplates
from .premises import PremisesShortList
from .role import ReadRole


class ReadUser(BaseModel):
    uuid: str
    name: Optional[str]
    email: EmailStr
    role: Optional[str]
    isActive: Optional[bool]


class ReadUsers(BaseModel):
    users: List[ReadUser]


class ReadUpdateUser(BaseModel):
    uuid: str
    name: Optional[str]
    email: EmailStr
    role: ReadRole
    isActive: Optional[bool]
    templates: List[dict]
    premises: List[dict]

class UserWithDetailsList(BaseModel):
    users: List[ReadUpdateUser]
from typing import Any, List, Optional
from uuid import UUID

from pydantic import UUID4, EmailStr, Json
from pydantic.networks import AnyHttpUrl

from .base import BaseModel, BaseOut, BaseOutName


class Template(BaseModel):
    pass


class CreateTemplate(BaseModel):
    pass


class UpdateTemplate(BaseModel):
    pass


class ReadTemplate(BaseModel):
    uuid: str
    name: str
    id: str
    creator: Any
    organization: Any


class ReadTemplates(BaseModel):
    templates: List[ReadTemplate]

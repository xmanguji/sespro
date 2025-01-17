from typing import List, Optional

from pydantic.types import UUID4, Json

from .base import BaseModel, BaseOut, BaseOutUuid


class CreateRole(BaseModel):
    pass


class UpdateRole(BaseModel):
    pass


class ReadRole(BaseModel):
    uuid: str
    name: str
    displayName: str


class ReadRoles(BaseModel):
    roles: List[ReadRole]

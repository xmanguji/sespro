from typing import Any, List, Optional
from uuid import UUID

from pydantic import UUID4, EmailStr, Json
from pydantic.networks import AnyHttpUrl

from .base import BaseModel, BaseOut, BaseOutName


class ManagerCreate(BaseModel):
    name: str
    email: EmailStr
    premises: Optional[List[Any]] = None


class PremisesCreate(BaseOutName):
    manager: ManagerCreate
    name: str
    group: Optional[UUID] = None


class ManagerUpdate(ManagerCreate):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ManagerOut(BaseOutName):
    email: EmailStr
    premises: List[PremisesCreate]


class AuditInProgress(BaseOut):
    user: UUID4
    premises: PremisesCreate
    data: Json


class PremisesUpdate(PremisesCreate):
    manager: Optional[ManagerCreate] = None
    name: Optional[str] = None
    group: Optional[UUID] = None


class PremisesOut(BaseOutName):
    manager: ManagerCreate
    users: List[AnyHttpUrl]
    group: Optional[UUID] = None
    audits_in_progress: List[Any]


class PremisesShort(BaseModel):
    name: str
    uuid: str


class PremisesShortList(BaseModel):
    premises: List[PremisesShort]


class ReadPremise(BaseModel):
    name: str
    uuid: str
    group: str
    group_uuid: str
    organization: Optional[str] = None


class ReadPremises(BaseModel):
    premises: List[ReadPremise]


class CreatePremises(BaseModel):
    uuid: str
    name: str
    render_enabled: bool


class ReadPremisesGroup(BaseModel):
    uuid: str
    name: str
    render_enabled: bool
    organization: str
    organization_uuid: str
    manager_name: str
    manager_uuid: str

class ReadPremisesGroups(BaseModel):
    groups: List[ReadPremisesGroup]


class CreatePremisesOrganization(BaseModel):
    pass


class UpdatePremisesOrganization(BaseModel):
    pass


class CreatePremisesGroup(BaseModel):
    pass


class UpdatePremisesGroup(BaseModel):
    pass


class ReadPremisesOrganization(BaseModel):
    uuid: str
    name: str
    render_enabled: bool


class ReadPremisesOrganizations(BaseModel):
    organizations: List[ReadPremisesOrganization]


class PremisesOrganization(BaseModel):
    uuid: str
    name: str
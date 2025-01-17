from typing import Optional, Set, List
from uuid import UUID

from pydantic import EmailStr

from .base import BaseModel, BaseOut, BaseOutName
from .premises import AuditInProgress, PremisesCreate, PremisesOrganization
from .templates import ReadTemplate


class EmailBase(BaseModel):
    email: EmailStr


class AuthBase(EmailBase):
    password: str


class LogIn(AuthBase):
    google: Optional[bool] = None


class Register(AuthBase):
    name: str


class UserUpdate(EmailBase):
    name: Optional[str] = None
    premises: Optional[PremisesCreate] = None
    audits_in_progress: Optional[Set[AuditInProgress]] = None
    active: Optional[bool] = None


class RegisterFull(Register):
    premises: Optional[PremisesCreate] = None
    audits_in_progress: Optional[Set[AuditInProgress]] = None
    active: bool = True


class RegisterOut(BaseOutName):
    email: EmailStr
    active: bool


class Token(BaseModel):
    token: str

class AdminToken(BaseModel):
    token: str
    userRole: Optional[str]
    organizations: Optional[List[PremisesOrganization]] = []
    templates: Optional[List[ReadTemplate]] = []
    userId: UUID


class ControlToken(BaseOut):
    user: UUID
    token: Optional[str] = None


class ResetPassword(BaseModel):
    password: str
    confirm: str
    token: str

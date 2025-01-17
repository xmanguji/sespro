from datetime import datetime
from typing import List, Optional

from pydantic.types import UUID4, Json
from pydantic.networks import EmailStr

from schema.base import BaseModel

from .auth import ControlToken


class ReturnControlToken(BaseModel):
    result: bool
    data: ControlToken


class Active(BaseModel):
    active: bool


class ForgetPassword(BaseModel):
    email: bool


class UpdateSchema(BaseModel):
    update: bool


class RegisteredSchema(BaseModel):
    registered: bool


class DeleteSchema(BaseModel):
    deleted: bool


class UploadImage(BaseModel):
    data: str


class UploadImageOut(BaseModel):
    upload: bool
    uuid: str
    uri: str


class DataIn(BaseModel):
    data: Json


class SubmitSchema(BaseModel):
    type: UUID4
    location: str
    final_comments: Optional[str]
    comments: Optional[str]
    extra: Optional[dict]
    stime: datetime
    etime: datetime
    body: List
    signatory: Optional[dict]
    timezone: Optional[str]


class ManagerSchema(BaseModel):
    uuid: UUID4
    name: str
    email: str

class EmailSchema(BaseModel):
    email: EmailStr

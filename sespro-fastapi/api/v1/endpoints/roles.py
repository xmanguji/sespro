import json
from uuid import UUID

from typing import List
from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session

from core.error import MissingResource
from core.security import get_current_active_user, logger
from crud import audits as crud_audits
from crud import premises as crud_premises
from crud import role as crud_role
from crud import user as crud_users
from model.user import User
from schema import ReadRoles, ReadRole

router = APIRouter(prefix="/roles")


@router.get("", response_model=ReadRoles, status_code=200)
@version(1, 0)
@db_session
def get_roles(user: User = Depends(get_current_active_user)):
    data = crud_role.get_roles()
    return {'roles': data}


import json
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session

from core.security import get_current_active_user, logger
from crud import templates as crud_templates
from model.user import User
from schema import ReadTemplates, ReadTemplate

router = APIRouter(prefix="/templates")


@router.get("", response_model=ReadTemplates, status_code=200)
@version(1, 0)
@db_session
def get_templates(user: User = Depends(get_current_active_user)):
    data = crud_templates.get_templates(user)
    return {'templates': data}


@router.post("", status_code=200)
@version(1, 0)
@db_session
def create_template(data: dict, user: User = Depends(get_current_active_user)):

    logger.info(f'Create | Template {json.dumps(data)}')

    response = crud_templates.create(obj_in=data)

    return {
        "created": 'true',
        "data": {
            'id': response.id,
            'name': response.name,
            'uuid': response.uuid
        }
    }


@router.put("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def update_template(data: dict, uuid: str, user: User = Depends(get_current_active_user)):

    db_obj = crud_templates.get_by_uuid(uuid=uuid)

    db_obj.set(**{"name": data.get("name")})
    db_obj.set(**{"organization": data.get("organization")})

    return {
        "updated": 'true'
    }


@router.delete("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def delete_template(uuid: str, user: User = Depends(get_current_active_user)):

    crud_templates.remove_by_uuid(uuid=uuid)

    return {
        "deleted": 'true'
    }
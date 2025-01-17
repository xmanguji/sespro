import json
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session, select, desc

from core.error import MissingResource
from core.security import get_current_active_user, logger
from crud import audits as crud_audits
from crud import premises as crud_premises
from crud import templates as crud_templates
from crud import role as crud_role
from crud import user as crud_users
from model.premises import PremisesGroup, PremisesOrganization
from model.user import User
from schema import ListAuditTemplateName, PremisesShortList, ReadUsers, ReadUpdateUser, UserWithDetailsList
from model import Role

router = APIRouter(prefix="/user")


@router.get("/premises", response_model=PremisesShortList, status_code=200)
@version(1, 0)
@db_session
def user_premises(user: User = Depends(get_current_active_user)):
    data = crud_premises.get_user_premises(user=user)
    return {'premises': data}


@router.get("/audits", response_model=ListAuditTemplateName, status_code=200)
@version(1, 0)
@db_session
def user_audits(user: User = Depends(get_current_active_user)):
    user = User.get(uuid=user.uuid)
    if not user.templates:
        raise MissingResource

    data = [{'uuid': str(t.uuid), 'name': t.name} for t in user.templates]

    return {'audits': data}


@router.get("/audit/{uuid}", status_code=200)
@version(1, 0)
@db_session
def user_get_audit(uuid: str, user: User = Depends(get_current_active_user)):
    uuid = UUID(uuid)

    template = crud_audits.get_by_uuid(uuid=uuid)

    if not template:
        raise MissingResource

    audit = template.build_audit()

    logger.info("=======================================================")
    logger.info("AUDIT GENERATED")
    logger.info("BY: %s", user.name)
    logger.info("FOR ONE OF THIS LOCATION")
    logger.info("%s", user.premises)
    logger.info("=======================================================")

    return {'body': audit}


@router.get('/session')
@version(1, 0)
def user_session_check(user: User = Depends(get_current_active_user)):
    return {}


@router.post("/clientlog", status_code=200)
@version(1, 0)
@db_session
def user_log(data: dict, user: User = Depends(get_current_active_user)):
    logger.info(f'CLIENT | USER {user.id} / {user.name} | {json.dumps(data)}')
    return {}


@router.get('/users')
@version(1, 0)
@db_session
def users(sortBy: str, sortDirection: str, perPage: int, currentPage: int = 0, user: User = Depends(get_current_active_user), organization: Optional[str] = None):
    
    user = User.get(uuid=user.uuid)
    role_name = Role[user.role.id]

    if organization is None or organization != 'null':
        organization_uuid = UUID(organization)
        query = select(u for u in User if (org.uuid == organization_uuid for org in u.premises_organization) and u.role.name != 'ROLE_ROOT')

    else:
        query = select(u for u in User)

    total_results = query.count()  

    users = []

    if sortDirection == 'desc':
        users = query.sort_by(desc(f'u.{sortBy}')).page(currentPage, perPage)

    else:
        users = query.order_by(f'u.{sortBy}').page(currentPage, perPage)      

    results = [
            {
                'uuid': str(u.uuid), 
                'name': str(u.name), 
                'email': u.email, 
                'role': str(u.role.displayName) if u.role is not None else '', 
                'isActive': u.active,
                'templates': [{'uuid': str(t.uuid), 'name': str(t.name)} for t in u.templates],
                'premises': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in u.premises],
                'groups': [{'uuid': str(group.uuid), 'name': str(group.name)} for group in u.premises_group],
                'organizations': [{'uuid': str(org.uuid), 'name': str(org.name)} for org in u.premises_organization]
            } 
            for u in users
        ]

    return {"total_results": total_results, "users": results }


@router.get('/managers')
@version(1, 0)
@db_session
def managers(user: User = Depends(get_current_active_user)):

    users = list(select(u for u in User if u.role.name == 'ROLE_MANAGER'))

    results = [
            {
                'uuid': str(u.uuid), 
                'name': str(u.name),
                'organizations': [{'uuid': str(org.uuid), 'name': str(org.name)} for org in u.premises_organization]
            } 
            for u in users
        ]

    return {"managers": results }


@router.post('', status_code=200)
@version(1, 0)
@db_session
def create_user(data: dict, user: User = Depends(get_current_active_user)):

    role_uuid = data["role"]

    if role_uuid != '':
        data["role"] = crud_role.get_by_uuid(uuid=role_uuid)
    else:
        data["role"] = crud_role.get_by_name(name='ROLE_AUDITOR')

    data["premises"] = [crud_premises.get_by_uuid(uuid=uuid) for uuid in data["premises"]]

    data["templates"] = [crud_templates.get_by_uuid(uuid=uuid) for uuid in data["templates"]]

    if "premises_group" in data:
        data["premises_group"] = PremisesGroup.get(uuid=data["premises_group"])

    if "premises_organization" in data:
        data["premises_organization"] = PremisesOrganization.get(uuid=data["premises_organization"])
    
    results = crud_users.create_new_user(obj_in=data)

    return {"created": 'true'}


@router.get('/{uuid}', response_model=ReadUpdateUser)
@version(1, 0)
@db_session
def get_user_details(uuid: str, user: User = Depends(get_current_active_user)):

    results = crud_users.get_user_details(uuid=uuid)

    return {"user", results}


@router.get('/details/{uuid}')
@version(1, 0)
@db_session
def get_user_details(uuid: str, user: User = Depends(get_current_active_user)):

    user_info = select(u for u in User if str(u.uuid) == str(uuid)).first()

    results = {
            'uuid': str(user_info.uuid),
            'name': str(user_info.name),
            'email': str(user_info.email),
            'role': {
                'name': str(user_info.role.name),
                'displayName': str(user_info.role.displayName),
                'uuid': str(user_info.role.uuid)
            },
            'isActive': user_info.active,
            'templates': [{'uuid': str(t.uuid), 'name': str(t.name)} for t in user_info.templates],
            'premises': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in user_info.premises],
            'groups': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in user_info.premises_group],
            'organizations': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in user_info.premises_organization]
        }

    return results


@router.delete('/{uuid}', status_code=200)
@version(1, 0)
@db_session
def delete_user(uuid: str, user: User = Depends(get_current_active_user)):

    results = crud_users.remove_by_uuid(uuid=uuid)

    return {
        "created": 'true'
    }

@router.post('/{uuid}', status_code=200)
@version(1, 0)
@db_session
def update_user(uuid: str, data: dict, current_user: User = Depends(get_current_active_user)):

    user = crud_users.get_by_uuid(uuid=uuid)

    user_data = {}

    if "name" in data:
        user_data["name"] = data["name"]

    if "email" in data:
        user_data["email"] = data["email"]
    
    if 'role' in data:
        user_data["role"] = crud_role.get_by_uuid(uuid=data["role"])

    if "premises" in data:
        user_data["premises"] = [crud_premises.get_by_uuid(uuid=uuid) for uuid in data["premises"]]

    if "templates" in data:
        user_data["templates"] = [crud_templates.get_by_uuid(uuid=uuid) for uuid in data["templates"]]

    if "premises_group" in data:
        user_data["premises_group"] = PremisesGroup.get(uuid=data["premises_group"])

    if "premises_organization" in data:
        user_data["premises_organization"] = PremisesOrganization.get(uuid=data["premises_organization"])

    if 'password' in data and data["password"] != "":
        crud_users.update_password(db_obj=user, password=data["password"])

    if user_data:
        user.set(**user_data)

    return {"updated": 'true'}
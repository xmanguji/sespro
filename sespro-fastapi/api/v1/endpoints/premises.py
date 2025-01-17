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
from crud import user as crud_users
from crud import group as crud_group
from crud import organization as crud_organization
from model.user import User
from model import PremisesGroup, PremisesOrganization
from schema import ListAuditTemplateName, PremisesShortList, ReadUsers, \
    ReadPremisesGroups, ReadPremisesOrganizations, ReadPremises, ReadPremise

router = APIRouter(prefix="/premises")


@router.get("/{sort}", response_model=ReadPremises, status_code=200)
@version(1, 0)
@db_session
def get_premises(sort: str = 'asc', user: User = Depends(get_current_active_user)):
    data = crud_premises.get_premises(sort=sort, user=user)
    return {'premises': data}


@router.post("", status_code=200)
@version(1, 0)
@db_session
def create_premises(data: dict, user: User = Depends(get_current_active_user)):

    logger.info(f'Create | Premises {json.dumps(data)}')

    group_uuid = data["group"]

    group = PremisesGroup.get(uuid=group_uuid)

    if group is not None:
        data["group"] = group

    response = crud_premises.create(obj_in=data)

    return {
        "created": 'true'
    }


@router.put("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def update_premises(data: dict, uuid: str, user: User = Depends(get_current_active_user)):

    db_obj = crud_premises.get_by_uuid(uuid=uuid)

    premises_group = crud_group.get_by_uuid(uuid=data.get("group"))

    db_obj.set(**{"group":premises_group, "name": data.get("name")})

    return {
        "updated": 'true'
    }


@router.delete("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def delete_premises(uuid: str, user: User = Depends(get_current_active_user)):

    crud_premises.remove_by_uuid(uuid=uuid)

    return {
        "deleted": 'true'
    }


@router.get("/groups/{sort}", response_model=ReadPremisesGroups, status_code=200)
@version(1, 0)
@db_session
def premises_groups(sort: str = 'asc', user: User = Depends(get_current_active_user)):

    results = crud_premises.get_groups(sort=sort, user=user)

    groups = [
        {'uuid': str(g.uuid), 'name': str(g.name), 'render_enabled': g.render_enabled,
         'organization': g.premises_organization.name if g.premises_organization is not None else '',
         'organization_uuid': str(g.premises_organization.uuid) if g.premises_organization is not None else '',
         'manager_name': str(crud_premises.get_group_manager(uuid=g.uuid).name) if crud_premises.get_group_manager(uuid=g.uuid) is not None else '',
         'manager_uuid': str(crud_premises.get_group_manager(uuid=g.uuid).uuid) if crud_premises.get_group_manager(uuid=g.uuid) is not None else ''} for g in
        results]

    return {
        'groups': groups
    }


@router.post("/groups", status_code=200)
@version(1, 0)
@db_session
def create_group(data: dict, user: User = Depends(get_current_active_user)):

    logger.info(f'Create | Premises Group {json.dumps(data)}')

    organization_uuid = data["premises_organization"]

    organization = None

    if organization_uuid != '':
        organization = PremisesOrganization.get(uuid=organization_uuid)

    manager_uuid = data["manager_uuid"]

    manager = None

    if manager_uuid != '':
        manager = User.get(uuid=manager_uuid)
    
    if manager is not None:
        data["users"] = manager

    data.pop("manager_uuid")
    data["premises_organization"] = organization
    print('------------->>>>>>>>>>>>>', data)
    response = crud_group.create(obj_in=data)

    return {
        "created": 'true'
    }

@router.put("/groups/{uuid}", status_code=200)
@version(1, 0)
@db_session
def update_premises_group(data: dict, uuid: str, user: User = Depends(get_current_active_user)):

    db_obj = crud_group.get_by_uuid(uuid=uuid)

    premises_organizations = crud_organization.get_by_uuid(uuid=data.get("premises_organization"))

    manager_uuid = data["manager_uuid"]

    manager = None

    if manager_uuid != '':
        manager = User.get(uuid=manager_uuid)
    
    if manager is not None:
        db_obj.set(**{"users": manager})

    db_obj.set(**{"premises_organization":premises_organizations, "name": data.get("name"), "render_enabled": data.get("render_enabled")})

    return {
        "updated": 'true'
    }


@router.delete("/groups/{uuid}", status_code=200)
@version(1, 0)
@db_session
def delete_group(uuid: str, user: User = Depends(get_current_active_user)):

    crud_group.remove_by_uuid(uuid=uuid)

    return {
        "deleted": 'true'
    }


@router.get("/organizations/{sort}", response_model=ReadPremisesOrganizations, status_code=200)
@version(1, 0)
@db_session
def premises_organizations(sort: str = 'asc', user: User = Depends(get_current_active_user)):

    results = crud_premises.get_organizations(sort=sort, user=user)

    organizations = [
        {'uuid': str(o.uuid), 'name': str(o.name), 'render_enabled': o.render_enabled} for o in results]

    return {'organizations': organizations}


@router.post("/organizations", status_code=200)
@version(1, 0)
@db_session
def create_organization(data: dict, user: User = Depends(get_current_active_user)):

    logger.info(f'Create | Premises Organization {json.dumps(data)}')

    response = crud_organization.create(obj_in=data)

    return {
        "created": 'true'
    }

@router.put("/organizations/{uuid}", status_code=200)
@version(1, 0)
@db_session
def update_premises_organization(data: dict, uuid: str, user: User = Depends(get_current_active_user)):

    db_obj = crud_organization.get_by_uuid(uuid=uuid)

    db_obj.set(**{"name": data.get("name"), "render_enabled": data.get("render_enabled")})

    return {
        "updated": 'true'
    }



@router.delete("/organizations/{uuid}", status_code=200)
@version(1, 0)
@db_session
def delete_organization(uuid: str, user: User = Depends(get_current_active_user)):

    crud_organization.remove_by_uuid(uuid=uuid)

    return {
        "deleted": 'true'
    }



import json
from uuid import UUID
from pony.orm import select, max

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session

from core.security import get_current_active_user, logger
from crud import category as crud_category
from model.user import User
from model import AuditTemplate, Category, AuditTemplateCategory, AuditTemplate
from schema import ReadCategories, CategoryCreate

router = APIRouter(prefix="/categories")


@router.get("/{template_id}", response_model=ReadCategories, status_code=200)
@version(1, 0)
@db_session
def get_categories(template_id: str, user: User = Depends(get_current_active_user)):
    data = crud_category.get_categories(template_id)
    return {'categories': data}


@router.post("/{template_id}", status_code=200)
@version(1, 0)
@db_session
def create_category(data: dict, template_id: str, user: User = Depends(get_current_active_user)):

    logger.info(f'Create | Category {json.dumps(data)}')

    audit_template = AuditTemplate.get(id=template_id)

    max_order = select(max(atc.order) for atc in AuditTemplateCategory if atc.audit_template == audit_template).first()
    order = max_order + 1 if max_order is not None else 0

    category = Category(text=data["text"], icon=data["icon"], color=data["color"])

    AuditTemplateCategory(audit_template=audit_template, category=category, order=order)

    # response = crud_category.create(obj_in=data)

    return {
        "created": 'true'
    }


@router.put("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def update_category(data: dict, uuid: str, user: User = Depends(get_current_active_user)):

    db_obj = crud_category.get_by_uuid(uuid=uuid)

    db_obj.set(**{"text": data.get("text")})

    return {
        "updated": 'true'
    }


@router.delete("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def delete_category(uuid: str, user: User = Depends(get_current_active_user)):

    crud_category.remove_by_uuid(uuid=uuid)

    return {
        "deleted": 'true'
    }



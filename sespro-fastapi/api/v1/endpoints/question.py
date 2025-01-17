import json

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session, select, max

from core.security import get_current_active_user, logger
from crud import question as crud_question
from model.user import User
from model import AuditTemplateQuestion, Question, AuditTemplate

router = APIRouter(prefix="/questions")


@router.post("", status_code=200)
@version(1, 0)
@db_session
def create_question(data: dict, user: User = Depends(get_current_active_user)):

    logger.info(f'Create | Question {json.dumps(data)}')

    audit_template = AuditTemplate.get(id=data.get('template_id'))

    max_order = select(max(atc.order) for atc in AuditTemplateQuestion if atc.audit_template == audit_template).first()
    order = max_order + 1 if max_order is not None else 1

    question = Question(text=data["text"], type=data["type"], category=data["category"], worth=data["worth"], weight=data["weight"], attachments=data["attachments"])

    AuditTemplateQuestion(audit_template=audit_template, question=question, order=order)

    return {
        "created": 'true'
    }


@router.put("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def update_question(data: dict, uuid: str, user: User = Depends(get_current_active_user)):

    db_obj = crud_question.get_by_uuid(uuid=uuid)

    db_obj.set(**{"text": data.get("text"), "weight": data.get("weight")})

    return {
        "updated": 'true'
    }


@router.delete("/{uuid}", status_code=200)
@version(1, 0)
@db_session
def delete_question(uuid: str, user: User = Depends(get_current_active_user)):

    crud_question.remove_by_uuid(uuid=uuid)

    return {
        "deleted": 'true'
    }



import json
import base64
import traceback
from http import HTTPStatus
from uuid import UUID, uuid4
from core.error import InvalidRequest, MissingPermission, MissingResource
from pony.orm.core import flush

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session, select, desc
from starlette import status
from starlette.responses import JSONResponse

from core.config import settings
from core.security import get_current_active_user, logger
from crud import audits as crud_templates
from crud import parsed as crud_parsed
from crud import premises as crud_premises
from crud import parsed_questions as crud_parsed_question
from crud import user as crud_user
from crud import question as crud_question
from model import User, ParsedAudit, ParsedQuestion, AuditImage
from schema import (DeleteSchema, SubmitSchema, UploadImage, UploadImageOut)
from schema.audit import AuditImageCreate
from utils.lambda_helper import invoke_emailer
from utils.s3_helper import get_raw_data
from utils.send_report import send_error_report
from utils.thumbnail_helper import make_thumbnails

from utils.s3_helper import (
    delete_image,
    get_image,
    get_raw_data,
    store_image,
    store_remapped_data,
)

router = APIRouter(prefix='/edit')


@router.get('/audits')
@version(1, 0)
@db_session
def get_editable_audits(sortBy: str, sortDirection: str, perPage: int, currentPage: int = 0, user: User = Depends(get_current_active_user)):
    """
    Get a list of parsed audits that can be edited

    Returns: A JSON array of objects containing the uuid, submit_time, template, and auditor
    """
    # TODO: more restrictive? less?
    user = User.get(uuid=user.uuid)
    premises = [p.uuid for p in user.premises]
    templates = [t.uuid for t in user.templates]
    templates = list(set(templates))

    # TODO: Replace with crud mechanism. Also pagination?

       
    query = None 

    if user.role is not None and user.role.name == 'ROLE_ROOT':
        query = select(p for p in ParsedAudit)
        
    else:
        user_premises_groups = list(user.premises_group)
        allowed_premises= [prem.uuid for prems in user_premises_groups for prem in prems.premises]
        allowed_premises = list(set(allowed_premises))
        query = select(p for p in ParsedAudit if (p.user is user.uuid or p.premises in allowed_premises) and p.audit_template.uuid in templates)
    
    total_results = query.count()

    if sortDirection == 'desc':
        audits = query.sort_by(desc(f'p.{sortBy}')).page(currentPage, perPage)

    else:
        audits = query.order_by(f'p.{sortBy}').page(currentPage, perPage)

    # audits = query.limit(perPage).offset(currentPage)
    

    data = []
    for audit in audits:
        template = audit.audit_template
        user = crud_user.get_by_uuid(uuid=audit.user)
        location = crud_premises.get_by_uuid(uuid=audit.premises)
        premises_data = {}
        if location:
            premises_data = {
                'uuid': location.uuid,
                'name': location.name
            }
        data.append({
            'uuid': audit.uuid,
            'submit_time': str(audit.date_submitted),
            'template': template.name if template else '',
            'auditor': user.name if user else '',
            'auditorUuid': user.uuid if  user else '',
            'premises': premises_data
        })
        # data.append({
        #     'uuid': audit.uuid,
        #     'submit_time': str(audit.date_submitted),
        #     'template': template.name if template else '',
        #     'auditor': user.name if user else '',
        #     'premises': {
        #         'uuid': location.uuid,
        #         'name': location.name
        #     }
        # })

    return {
            "audits": data,
            "total_results": total_results
        }


@router.get('/audit/{uuid}')
@version(1, 0)
@db_session
def get_editable_audit(uuid: UUID, _: User = Depends(get_current_active_user)):
    """
    Gets the full data of a parsed audit by UUID

    Args:
        uuid: The parsed audit UUID to fetch

    Returns: The raw submitted content of the requested audit from a client application
    """
    scored_audit = crud_parsed.get_by_uuid(uuid=uuid)
    raw_data_key = scored_audit.raw_data_key
    res = get_raw_data(key=raw_data_key)
    if not res["success"]:
        return JSONResponse(
            status_code=404,
            content={'message': 'could not retrieve raw audit data'})

    raw_obj = res["obj_json"].read().decode("utf-8")
    raw_obj = json.loads(raw_obj)
    
    raw_obj['etime'] = scored_audit.end_time
    raw_obj['type'] = scored_audit.audit_template.uuid
    raw_obj['location'] = scored_audit.premises
    return raw_obj


@router.post('/audit/{uuid}')
@version(1, 0)
@db_session
def save_editable_audit(edited_audit: SubmitSchema,
                        uuid: UUID,
                        user: User = Depends(get_current_active_user)):
    """
    Save edits to a raw audit over a parsed audit in the database by UUID

    Args:
        edited_audit: The raw audit data to be resubmitted
        uuid: The parsed audit UUID this is for

    Returns: A JSON response with a 'saved' key representing the boolean status of saving this audit
    """
    # TODO: add parsing for updating more than notes
    # TODO: add CRUD for updating
    logger.info(
        f"[EDITOR] Attempting to save edited audit / User: {user.name}")
    parsed_audit = crud_parsed.get_by_uuid(uuid=uuid)
    # Parse questions

    parsed_audit.premises = UUID(edited_audit.location)

    for category in edited_audit.body:
        for question in category['questions']:
            parsed_question = crud_question.get_by_uuid(uuid=question['uuid'])
            pq = ParsedQuestion.select(question=parsed_question,
                                        parsed_audit=parsed_audit)
            if 'notes' in question:
                pq.notes = question['note']
            if 'passed' in question:
                pq.passed = question['passed']

    return {'saved': True}


@router.get('/render/{uuid}')
@version(1, 0)
@db_session
def render_audit(uuid: UUID, user: User = Depends(get_current_active_user)):
    """
    Forcibly render and email an audit by UUID

    Args:
        uuid: The parsed audit UUID

    Returns: A JSON response with a 'pdf' key representing the boolean status of creating and sending the PDF
    """
    scored_audit = crud_parsed.get_by_uuid(uuid=uuid)

    auditor = crud_user.get_by_uuid(uuid=scored_audit.user)

    template = crud_templates.get_by_uuid(uuid=scored_audit.audit_template.uuid)

    location = crud_premises.get_by_uuid(uuid=scored_audit.premises)
    
    render_url = f'{settings.RENDER_BASE_URL}/audit/render/{str(uuid)}?user={str(auditor.uuid)}'

    premises_group = location.group

    is_render_enabled = True

    if hasattr(premises_group, "render_enabled") and premises_group.render_enabled is not None:
        is_render_enabled = premises_group.render_enabled

    if is_render_enabled:
        send_to_emails = [u.email if u.role.name == 'ROLE_MANAGER' else '' for u in premises_group.users] if premises_group is not None else []

        if settings.SEND_TO_AUDITOR:
            send_to_emails.append(auditor.email)

        filterd_emails = [email for email in send_to_emails if email]
        to_emails = (filterd_emails)

    try:
        logger.info(f'[LAMBDA/EDITOR] Calling for {render_url}')
        lambda_result = invoke_emailer(
            url=render_url,
            uuid=str(uuid),
            report_id=str(uuid),
            template_name=template.name,
            auditor=auditor.name,
            site=location.name,
            score=f'{(scored_audit.score_percentage * 100):.0f}%',
            to_emails=to_emails,
            bcc_emails=settings.EXTRA_BCC_EMAILS)

        if not lambda_result:
            raise Exception(
                f'Could not call lambda function {settings.EMAILER_LAMBDA}')

        logger.info(
            "=======================================================")
        logger.info("EMAILER LAUNCHED")
        logger.info("TO:")
        logger.info(to_emails)
        logger.info("BCC:")
        logger.info(settings.EXTRA_BCC_EMAILS)
        logger.info("EMAILER LOCATION: %s", location.name)
        logger.info("EMAILER AUDIT ID: %s", scored_audit.uuid)
        logger.info(
            "=======================================================")
    except:
        e_msg = traceback.format_exc()
        logger.error(
            "=======================================================")
        logger.error("ERROR LAUNCHING EMAILER")
        logger.error(e_msg)
        logger.error(
            "=======================================================")
        send_error_report(traceback=e_msg,
                          from_email=settings.AWS_SES_SENDER,
                          to_emails=settings.ERROR_EMAILS,
                          subject=f'{settings.API_TITLE} API Error')
        return JSONResponse(content={'pdf': False},
                            status_code=status.HTTP_202_ACCEPTED)
    # End report generation
    return {'pdf': True}


@router.delete("/audit/{parsed_uuid}", response_model=DeleteSchema, status_code=HTTPStatus.ACCEPTED)
@version(1, 0)
@db_session
def delete_submitted_audit(parsed_uuid: str, _: User = Depends(get_current_active_user)):
    parsed_audit_uuid = UUID(parsed_uuid)

    persisted_audit = crud_parsed.get_by_uuid(uuid=parsed_audit_uuid)

    if persisted_audit is None:
        return JSONResponse(status_code=404,
                            content={'message': 'Audit response not found'})

    # TODO: validate user allowed to do the delete transaction

    crud_parsed.remove_by_uuid(uuid=parsed_audit_uuid)

    return {"deleted": True}

@router.post(
    "/image/{parsed_audit}/{location}/{parsed_question}", response_model=UploadImageOut, status_code=200
)
@version(1, 0)
@db_session
def upload_image(
    parsed_audit, location, parsed_question, data: UploadImage, user: User = Depends(get_current_active_user)
):

    location = UUID(location)
    parsed_question_uuid = UUID(parsed_question)

    pq = crud_parsed_question.get_by_uuid(uuid=parsed_question)
    p = crud_premises.get_by_uuid(uuid=location)

    if not pq:
        pq = crud_parsed_question.get_by_question_and_audit(question=parsed_question, audit=parsed_audit)

    if not p or not pq:
        logger.error("UUIDs not valid for image upload")
        raise MissingResource

    persisted_image = None

    q = pq.question

    
    images = pq.images

    if images:
        images = list(images)
        for img in images:
            image_uuid = img.uuid
            response = makeImage(uuid=str(image_uuid), data=data)
            uri, full_name = response["uri"], response["image_key"]
            update_json = {"image_uri": uri, "image_key": full_name}
            img.set(**update_json)
                
            persisted_image = img

    else:
        image_uuid = uuid4()
        response = makeImage(uuid=str(image_uuid), data=data)
        uri, full_name = response["uri"], response["image_key"]
        dbi = AuditImageCreate(uuid=image_uuid, user=user.uuid, premises=p.uuid, question=q.uuid, image_uri=uri, image_key=full_name)
        dbi.parsed_question = parsed_question_uuid
        if pq.parsed_audit:
            dbi.parsed_audit = pq.parsed_audit.uuid

        persisted_image = crud_templates.create_image(obj_in=dbi)

    
    if not persisted_image:
        logger.error("Unable to store the image")
        raise MissingResource
    
    flush()

    return {"upload": True, "uuid": str(persisted_image.uuid), 'uri': str(persisted_image.image_uri)}

def makeImage(uuid: str, data: UploadImage):
    img = data.data.encode("ascii")

    temp_image = base64.b64decode(img)
    thumbnailed_img = make_thumbnails(
        image=temp_image,
        thumbnails_dim=(settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT),
    )
    if not thumbnailed_img:
        raise InvalidRequest

    response = store_image(image=thumbnailed_img, uuid=str(uuid))

    if not response["success"]:
        return JSONResponse(
            status_code=422,
            content={"message": "An Error Ocuured When Uploading Image"},
        )

    return response

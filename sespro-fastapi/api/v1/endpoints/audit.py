import base64
import json
import traceback
from pathlib import Path
from uuid import UUID, uuid4
from pony.orm.core import flush

from core.config import settings
from core.error import InvalidRequest, MissingPermission, MissingResource
from core.security import get_current_active_user, logger
from crud import audits as crud_audit
from crud import parsed as crud_parsed
from crud import premises as crud_premise
from crud import question as crud_question
from crud import parsed_questions as crud_parsed_question
from crud import user as crud_user
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi_versioning import version
from jinja2 import Environment, FileSystemLoader, select_autoescape
from model.user import User
from pony.orm import commit, db_session
from schema import DataIn, DeleteSchema, SubmitSchema, UploadImage, UploadImageOut
from schema.audit import AuditImageCreate
from starlette.responses import HTMLResponse, JSONResponse
from utils.helpers import remap, save_parsed_audit, update_images
from utils.lambda_helper import invoke_emailer
from utils.s3_helper import (
    delete_image,
    get_image,
    get_raw_data,
    store_image,
    store_remapped_data,
)
from utils.send_report import send_error_report
from utils.thumbnail_helper import make_thumbnails
import requests

"""from utils.send_report import (_send_debug_report, generate_email_filename,
                               generate_report_body, generate_report_subject,
                               send_audit_report)"""

UK_DATE_FORMAT = "%d %B %Y at %H:%M"

root_environment_path: str = Path.cwd()
root_template_path: str = root_environment_path / "templates"
root_static_path: str = root_environment_path / "static"

router = APIRouter(prefix="/audit")


@router.get("/photo/{photo}")
@version(1, 0)
@db_session
def retrieve_image(photo: str):
    try:
        photo = UUID(photo)

    except:
        return JSONResponse(status_code=400, content={"message": "Invalid request"})

    d_img = crud_audit.get_image_by_uuid(uuid=photo)

    if not d_img:
        return JSONResponse(
            status_code=422,
            content={"message": "No such resource by that UUID or name"},
        )

    image_key = d_img.image_key

    res = get_image(full_name=image_key)

    if not res["success"]:
        return JSONResponse(
            status_code=422, content={"message": "Could not retrive image"}
        )

    data = res["image_byte"].read()
    """fake_ptr = BytesIO()
    fake_ptr.write(base64.b64decode(data))
    fake_ptr.seek(0)"""

    return Response(data, media_type="image/jpeg")


@router.delete("/photo/{photo}", response_model=DeleteSchema, status_code=200)
@version(1, 0)
@db_session
def remove_image(photo: str, user: User = Depends(get_current_active_user)):

    d_img = crud_audit.get_image_by_uuid(uuid=UUID(photo))

    if not d_img:
        return JSONResponse(
            status_code=422,
            content={"message": "No such resource by that UUID or name"},
        )

    if user.uuid != d_img.user and not crud_user.hasAdminRole(uuid=str(user.uuid)):
        return JSONResponse(
            status_code=400, content={"message": "No permissions for resource"}
        )

    if not crud_audit.remove_image(db_obj=d_img):
        return {"deleted": False}
    res = delete_image(full_name=d_img.image_key)
    if not res["success"]:
        return {"deleted": False}
    return {"deleted": True}


@router.post(
    "/image/{location}/{question}", response_model=UploadImageOut, status_code=200
)
@version(1, 0)
@db_session
def upload_image(
    location, question, data: UploadImage, user: User = Depends(get_current_active_user)
):

    location = UUID(location)
    question = UUID(question)

    q = crud_question.get_by_uuid(uuid=question)
    p = crud_premise.get_by_uuid(uuid=location)

    if not p or not q:
        logger.error("UUIDs not valid for image upload")
        raise MissingResource
     
    image_uuid = uuid4()
    response = makeImage(uuid=str(image_uuid), data=data)
    uri, full_name = response["uri"], response["image_key"]             
    dbi = AuditImageCreate(uuid=image_uuid,user=user.uuid,premises=p.uuid,question=q.uuid,image_uri=uri,image_key=full_name)    

    persisted_image = None
    
    if dbi:
        persisted_image = crud_audit.create_image(obj_in=dbi)
        flush()

    if not persisted_image:
        logger.error("Unable to store the image")
        raise MissingResource
    
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



@router.post("/submit", status_code=200)
@version(1, 0)
@db_session
def audit_submission(
    request: Request,
    obj_in: SubmitSchema,
    user: User = Depends(get_current_active_user),
):

    # Get Timezone
    timezone = 'America/Denver'
    # response = requests.get(f"https://ipinfo.io/{request.client.host}/json")
    # timezone=settings.API_TIMEZONE
    # if response.status_code == 200:
    #     data = response.json()
    #     timezone = data.get("timezone")

    print('timezone body =============> ', timezone)

    obj_in.timezone = timezone
    result = save_parsed_audit(obj_in=obj_in, user=user)

    premises = crud_premise.get_by_uuid(uuid=UUID(obj_in.location))
    location_name = premises.name
    
    print('location_name =============> ', location_name)
    premises_group = premises.group

    if not result["success"]:
        return JSONResponse(
            status_code=result["status_code"], content={"message": result["message"]}
        )
    else:
        # NOTE: This is an explicit commit to ensure data is available to the renderer
        logger.info(f"Audit from {user.name} parsed and saved")
        commit()

    result = result["result"]
    logger.info(result)
    recepients = settings.EXTRA_BCC_EMAILS
    # stupid_object = result["final_remap"]
    location = result["location"]
    scored_audit = result["scored_audit"]

    template = crud_audit.get_by_uuid(uuid=scored_audit.audit_template.uuid)

    logger.info("=======================================================")
    logger.info("AUDIT SUBMITTED")
    logger.info("BY: %s", user.name)
    logger.info("FOR:")
    logger.info("LOCATION: %s", location_name)
    logger.info("AUDIT ID: %s", scored_audit.uuid)
    logger.info("=======================================================")

    update_images(
        obj_in=obj_in, scored_audit=scored_audit, user=user.uuid, location=location.uuid
    )

    # By default premises group enabled
    is_render_enabled = True

    # if hasattr(premises_group, "render_enabled") and premises_group.render_enabled is not None:
    #     is_render_enabled = premises_group.render_enabled

    print('premises_group.users =============> ', premises_group.users)

    if is_render_enabled:
        render_url = f"{settings.RENDER_BASE_URL}/audit/render/{str(scored_audit.uuid)}?user={str(user.uuid)}"
        send_to_emails = [u.email if u.role.name == 'ROLE_MANAGER' else '' for u in premises_group.users] if premises_group is not None else []
        print('render url =============> timezone and', timezone , ' ==== ', render_url)
        if settings.SEND_TO_AUDITOR:
            send_to_emails.append(user.email)

        filterd_emails = [email for email in send_to_emails if email]
        to_emails = (filterd_emails)
        print('==============> sender emails =============>', to_emails)
        try:
            logger.info(f"[LAMBDA] Calling for {render_url}")
            lambda_result = invoke_emailer(
                url=render_url,
                uuid=str(scored_audit.uuid),
                report_id=str(scored_audit.uuid),
                auditor=user.name,
                template_name=template.name,
                site=location.name,
                score=f"{(scored_audit.score_percentage * 100):.0f}%",
                to_emails=to_emails,
                bcc_emails=recepients,
            )

            if not lambda_result:
                raise Exception(
                    f"Could not call lambda function {settings.EMAILER_LAMBDA}"
                )

            logger.info("=======================================================")
            logger.info("EMAILER LAUNCHED")
            logger.info("TO:")
            logger.info(to_emails)
            logger.info("BCC:")
            logger.info(settings.EXTRA_BCC_EMAILS)
            logger.info("EMAILER LOCATION: %s", location_name)
            logger.info("EMAILER AUDIT ID: %s", scored_audit.uuid)
            logger.info("=======================================================")
        except:
            e_msg = traceback.format_exc()
            logger.error("=======================================================")
            logger.error("ERROR LAUNCHING EMAILER")
            logger.error(e_msg)
            logger.error("=======================================================")
            send_error_report(
                traceback=e_msg,
                from_email=settings.AWS_SES_SENDER,
                to_emails=settings.ERROR_EMAILS,
                subject=f"{settings.API_TITLE} API Error",
            )
            return JSONResponse(
                content={"pdf": False}, status_code=status.HTTP_202_ACCEPTED
            )
        # End report generation
        return {"pdf": True}
    else:
        return {"pdf": True}


@router.put("/progress/{uuid}", status_code=204)
@version(1, 0)
@db_session
def update_audit_progress(
    uuid: str, obj_in: DataIn, user: User = Depends(get_current_active_user)
):

    uuid = UUID(uuid)

    premises = crud_premise.get_by_uuid(uuid=uuid)

    if not premises:
        raise MissingResource

    if user not in premises.users:
        raise MissingPermission

    save_state = crud_audit.get_audit_progress_by_uuid(uuid=uuid)

    if not save_state:
        data = {"user": user, "premises": premises, "data": obj_in.data}
        save_state = crud_audit.create_audit_progress(**data)
    else:
        data = {"data": obj_in.data}
        crud_audit.update_audit_progress(obj_in=data, db_obj=save_state)
    return {}


@router.get("/progress/{uuid}", response_model=DataIn, status_code=200)
@version(1, 0)
@db_session
def get_audit_progress(uuid: str, user: User = Depends(get_current_active_user)):

    uuid = UUID(uuid)

    premises = crud_premise.get_by_uuid(uuid=uuid)

    if not premises:
        raise MissingResource

    if user not in premises.users:
        raise MissingPermission

    save_state = crud_audit.get_audit_progress_by_uuid(uuid=uuid)

    if not save_state:
        raise MissingResource
    return save_state.data


@router.get("/render/{uuid}", response_class=HTMLResponse)
@version(1, 0)
@db_session
def render_audit_html(uuid: str, user: str):
    uuid = UUID(uuid)
    user = UUID(user)

    jinja_env = Environment(
        autoescape=select_autoescape(enabled_extensions=[]),
        loader=FileSystemLoader(searchpath=root_template_path),
    )

    scored_audit = crud_parsed.get_by_uuid(uuid=uuid)

    user = crud_user.get_by_uuid(uuid=user)

    raw_data_key = scored_audit.raw_data_key
    res = get_raw_data(key=raw_data_key)
    if not res["success"]:
        return JSONResponse(
            status_code=404, content={"message": "could not retrive data"}
        )
    raw_obj = res["obj_json"].read().decode("utf-8")
    raw_obj = json.loads(raw_obj)

    obj_in = SubmitSchema(**raw_obj)

    data = remap(scored_audit=scored_audit, user=user, obj_in=obj_in)

    final_remap = json.loads(data["final_remap"])

    location = data["location"]

    save_remaped = store_remapped_data(
        location=location.name, _object=data["final_remap"]
    )

    logger.info(final_remap)

    header_html = jinja_env.get_template(settings.RENDER_TEMPLATE).render(
        audit_data=final_remap
    )

    return header_html

import base64
from uuid import UUID

from core.config import settings
from core.error import InvalidRequest, MissingResource
from core.security import get_current_active_user, logger
from crud import audits as crud_audit
from crud import category as crud_category
from crud import parsed as crud_parsed
from crud import premises as crud_premise
from crud import question as crud_question
from crud import parsed_questions as crud_parsed_question
from fastapi import APIRouter, Depends
from fastapi_versioning import version
from model import ParsedQuestion, User
from model.parsed import AuditImage
from pony.orm import db_session
from schema import SubmitSchema
from schema.utils import UploadImage
from starlette.responses import JSONResponse
from utils.helpers import update_images_by_editor, update_parsed_audit
from utils.s3_helper import delete_image, delete_raw_data, store_image
from utils.thumbnail_helper import make_thumbnails
from model.user import User

router = APIRouter(prefix="/edit")


@router.post("/audit/{uuid}")
@version(2, 0)
@db_session
def save_editable_audit(
    edited_audit: SubmitSchema,
    uuid: UUID,
    user: User = Depends(get_current_active_user),
):
    """
    Save edits to a raw audit over a parsed audit in the database by UUID

    Args:
        edited_audit: The raw audit data to be resubmitted
        uuid: The parsed audit UUID this is for

    Returns: A JSON response with a 'saved' key representing the boolean status of saving this audit
    """
    # TODO: add parsing for updating more than notes
    # TODO: add CRUD for updating
    logger.info(f"[EDITOR] Attempting to save edited audit / User: {user.name}")
    parsed_audit = crud_parsed.get_by_uuid(uuid=uuid)
    auditor = User.get(uuid=parsed_audit.user)

    if 'category' in edited_audit.body:
        for category in edited_audit.body:
            for question in category['questions']:

                persisted_pq = crud_parsed_question.get_by_question_and_audit(question=str(question["uuid"]), audit=str(uuid))

                if not persisted_pq:
                    persisted_pq = crud_parsed_question.get_by_uuid(uuid=question['uuid'])

                if persisted_pq:                
                    persisted_pq.set(notes=question['notes'], passed=question['passed'])
    else:
        for item in edited_audit.body:
            for question in item['questions']:
                
                persisted_pq = crud_parsed_question.get_by_question_and_audit(question=str(question["uuid"]), audit=str(parsed_audit.uuid))
            
                if not persisted_pq:
                    persisted_pq = crud_parsed_question.get_by_uuid(uuid=question['uuid'])

                if persisted_pq and 'pass' in question:                
                    persisted_pq.set(passed=question['pass'])

    result = update_parsed_audit(
        obj_in=edited_audit, user=auditor, parsed_audit=parsed_audit
    )
    
    result = result["result"]
    location = result["location"]
    scored_audit = result["scored_audit"]

    logger.info("=======================================================")
    logger.info("AUDIT UPDATE SUBMITTED")
    logger.info("BY: %s", user.name)
    logger.info("FOR:")
    logger.info("LOCATION: %s", location.name)
    logger.info("AUDIT ID: %s", scored_audit.uuid)
    logger.info("=======================================================")

    return {"saved": True}


@router.delete("/audit/{uuid}")
@version(2, 0)
@db_session
def delete_audit(
    uuid: UUID,
    user: User = Depends(get_current_active_user),
):
    parsed_audit = crud_parsed.get_by_uuid(uuid=uuid)
    if parsed_audit.user != user.uuid:
        premises = crud_premise.get_by_uuid(uuid=uuid)
        if parsed_audit.user != premises.manager.uuid:
            return JSONResponse(
                status_code=403,
                content={"message": "You are not permitted to delete this audit"},
            )

    raw_data_key = parsed_audit.raw_data_key
    result = delete_raw_data(full_name=raw_data_key)

    if not result["success"]:
        return JSONResponse(
            status_code=400,
            content={"message": "Error deleting resource"},
        )

    parsed_audit.delete()

    delete_raw_data(full_name=raw_data_key)

    return {"deleted": True}


@router.put("/photo/{photo}")
@version(2, 0)
@db_session
def update_image(
    photo: str, data: UploadImage, user: User = Depends(get_current_active_user)
):
    try:
        photo = UUID(photo)

    except:
        return JSONResponse(status_code=400, content={"message": "Invalid request"})

    d_img: AuditImage = crud_audit.get_image_by_uuid(uuid=photo)

    if not d_img:
        return JSONResponse(
            status_code=422,
            content={"message": "No such resource by that UUID or name"},
        )

    image_key = d_img.image_key

    q = crud_question.get_by_uuid(uuid=d_img.question)

    p = crud_premise.get_by_uuid(uuid=d_img.premises)

    if not p or not q:
        logger.error("UUIDs not valid for image upload")
        raise MissingResource

    if user.uuid != d_img.user:
        return JSONResponse(
            status_code=400, content={"message": "No permissions for resource"}
        )

    img = data.data.encode("ascii")

    temp_image = base64.b64decode(img)
    thumbnailed_img = make_thumbnails(
        image=temp_image,
        thumbnails_dim=(settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT),
    )
    if not thumbnailed_img:
        raise InvalidRequest

    response = store_image(thumbnailed_img)

    if not response["success"]:
        return JSONResponse(
            status_code=422,
            content={"message": "An Error Ocuured When Uploading Image"},
        )

    uri, full_name = response["uri"], response["image_key"]

    d_img.set(image_key=full_name, image_uri=uri)

    delete_image(full_name=image_key)

    return {"upload": True, "uuid": str(d_img.uuid)}


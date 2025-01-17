from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from pony.orm.core import db_session

from core.config import settings
from core.error import InactiveAccount, InvalidLogin, InvalidRequest
from core.security import generate_login_token, get_current_active_user, logger
from crud import user as crud_user
# from etllib.notifications import report_email
from model.user import User
from schema import Active
from schema import ControlToken as Schema_CT
from schema import (
    EmailBase,
    ForgetPassword,
    LogIn,
    Register,
    RegisteredSchema,
    ResetPassword,
    Token,
    UpdateSchema,
    AdminToken
)

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token, status_code=200)
@version(1, 0)
@db_session
def log_in(form_data: OAuth2PasswordRequestForm = Depends()):
    """The login end point

    Args:
        credential (LogIn): {email: Emailstr, "password": str, "google[optional]": bool}

    Raises:
        InvalidLogin: Inavlid Login crendentials
        InactiveAccount: The account is not active

    Returns:
        Token: The token generated
    """
    user = crud_user.get_by_email(email=form_data.username)

    if user is None:
        raise InvalidLogin

    if not user.check_password(form_data.password):
        raise InvalidLogin

    if not user.active:
        raise InactiveAccount
    logger.info(f"User: '{user.name}'' with email '{user.email} just logged in")
    return {"token": generate_login_token(user.id)}

@router.post("/login/admin", response_model=AdminToken, status_code=200)
@version(1, 0)
@db_session
def log_in(form_data: OAuth2PasswordRequestForm = Depends()):
    """The login end point

    Args:
        credential (LogIn): {email: Emailstr, "password": str, "google[optional]": bool}

    Raises:
        InvalidLogin: Inavlid Login crendentials
        InactiveAccount: The account is not active

    Returns:
        Token: The token generated
    """
    user = crud_user.get_by_email(email=form_data.username)

    if user is None:
        raise InvalidLogin

    if not user.check_password(form_data.password):
        raise InvalidLogin

    if not user.active:
        raise InactiveAccount


    # if user.role.name != 'ROLE_ROOT' and user.role.name != 'ROLE_MANAGER':
    #     raise InactiveAccount
    
    logger.info(f"User: '{user.name}'' with email '{user.email} just logged in")
    return {
        "token": generate_login_token(user.id),
        "userRole": user.role.name,
        'organizations': [{'uuid': str(org.uuid), 'name': str(org.name)} for org in user.premises_organization],
        'templates': [{'uuid': str(org.uuid), 'name': str(org.name), 'id': str(org.id)} for org in user.templates],
        "userId": user.uuid
    }



@router.get("/logout", status_code=204)
@version(1, 0)
async def log_out(user: User = Depends(get_current_active_user)):
    logger.info(f"User: '{user.name}'' with email '{user.email} just logged out")
    return {}


@router.get("/activate/{token}", response_model=Active, status_code=200)
@version(1, 0)
@db_session
def activate_user(token: str):
    """Verify and activate account

    Args:
        token (str): activation token

    Raises:
        InvalidRequest: [description]
        MissingResource: [description]

    Returns:
        [type]: [description]
    """

    t = crud_user.get_token(token=token)

    if not t:
        raise InvalidRequest

    user = crud_user.activate_account(uuid=t.user)

    crud_user.delete_verification_token(t=t)

    return {"active": True}


@router.post("/forgot", response_model=ForgetPassword, status_code=200)
@version(1, 0)
@db_session
def forgot_password(email_data: EmailBase):
    """Verify and activate account

    Args:
        email (Email): The User email Address

    Raises:
        InvalidRequest: [description]
        MissingResource: [description]

    Returns:
        [type]: [description]

    """

    email = email_data.email

    user = crud_user.get_by_email(email=email)

    if not email:
        raise InvalidRequest

    t = crud_user.get_token(uuid=user.uuid)
    if not t:
        t = crud_user.create_token(obj_in=Schema_CT(user=user.uuid))

    email = {
        "subject": f"{settings.API_TITLE} - Password Reset",
        "from": settings.AWS_SES_SENDER,
    }

    url = f"{settings.CLIENT_BASE_URL}/reset/{t.token}"

    email[
        "msg"
    ] = f"""Here is your password reset link.
    
    {url}
    """

    logger.info(t.token)
    logger.info(email["subject"], email["msg"], email["from"], [user.email.lower()])

    return {"email": True}


@router.post("/reset", response_model=UpdateSchema, status_code=200)
@version(1, 0)
@db_session
def reset_password(reset_data: ResetPassword):

    t = crud_user.get_token(token=reset_data.token)
    if not t:
        raise InvalidRequest

    if reset_data.password != reset_data.confirm:
        raise InvalidRequest

    user = crud_user.get_by_uuid(uuid=t.user)

    if not user:
        raise InvalidRequest

    crud_user.update_password(db_obj=user, password=reset_data.password)
    crud_user.delete_verification_token(t=t)

    email = {
        "subject": f"{settings.API_TITLE} - Password Changed",
        "from": settings.AWS_SES_SENDER,
        "msg": "Your password was changed.",
    }

    # report_email(email['subject'], email['msg'], email['from'], [u.email.lower()])

    return {"update": True}


@router.post("/register", response_model=RegisteredSchema, status_code=201)
@version(1, 0)
@db_session
def register(reg_data: Register):

    if crud_user.get_by_email(email=reg_data.email):
        raise InvalidRequest

    user = reg_data.dict()
    user = crud_user.create(obj_in=user)

    email = {
        "subject": f"{settings.API_TITLE} - Activate Account",
        "from": settings.AWS_SES_SENDER,
    }

    url = f"{settings.CLIENT_BASE_URL}/activate/{user.token.token}"

    email[
        "msg"
    ] = f"""Thank you for registering for {settings.API_TITLE}.
    
    To activate your account, use the link below.

    {url}
    """

    logger.info(user.token.token)

    # report_email(email['subject'], email['msg'], email['from'], [user.email.lower()])

    return {"registered": True}

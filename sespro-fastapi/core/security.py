from core.error import InvalidToken, NotAuthenticated
import logging
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from fastapi import Header
from pony.orm import db_session

import crud

from .config import settings
from crud import user as crud_user

logger = logging.getLogger(__name__)


def days_in_the_future(days: int) -> datetime:
    return datetime.utcnow() + timedelta(days=days)


def generate_login_token(user_id: int, expires_delta: Optional[timedelta] = None):
    """Helps generate auth token

    Args:
        user_id (int): The user primary key
        expires_delta (Optional[timedelta], optional): The token life span. Defaults to None.

    Returns:
        [type]: The generated Token
    """

    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = days_in_the_future(-180)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET, algorithm="HS256")


def unpack_login_token(token: str) -> int:
    """Decode Token

    Args:
        token (str): the token

    Raises:
        InvalidToken: The token doesn't have decodeable payload
        NotAuthenticated: User not registered

    Returns:
        int: the user_id
    """

    try:
        unpacked = jwt.decode(token, settings.SECRET, options={"verify_exp": False})
    except JWTError:
        logger.info(f"Authentication failed with token: {token}")
        raise InvalidToken()

    user_id: int = int(unpacked.get("sub"))
    if user_id is None:
        raise NotAuthenticated()

    return user_id


@db_session
def get_current_active_user(authorization: str = Header(None)):
    # TODO: add prefetching of relevant user information
    try:
        auth_header = authorization

        token = auth_header.split("Bearer ", 1)[1]
    except KeyError:
        raise NotAuthenticated()
    except IndexError:
        logger.info(f"Authentication failed with malformed header: {authorization}")
        raise NotAuthenticated()

    try:
        user_id: int = unpack_login_token(token)
    except JWTError:
        logger.info(f"Authentication failed with token: {token}")
        raise InvalidToken()

    user = crud_user.get(id=user_id)

    if user is None or not user.active:
        raise NotAuthenticated()

    return user

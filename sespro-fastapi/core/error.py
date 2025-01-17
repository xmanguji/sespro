from starlette.requests import Request
from starlette.responses import JSONResponse


class InvalidRequest(Exception):
    pass


# The object does not exist in the database when queried by ID or name
class MissingResource(Exception):
    pass


# It exists, but the user does not have permission to do anything with it
class MissingPermission(Exception):
    pass


class InvalidLogin(Exception):
    pass


class InactiveAccount(Exception):
    pass


class InvalidToken(Exception):
    pass


class NotAuthenticated(Exception):
    pass


async def not_authenticated_exception_handler(request: Request, exc: NotAuthenticated):
    return JSONResponse(status_code=401, content={"message": "Not authenticated"})


async def invalid_token_exception_handler(request: Request, exc: InvalidToken):
    return JSONResponse(
        status_code=401, content={"message": "Not authenticated, Invalid Token"}
    )


async def inactive_account_exception_handler(
    request: Request, exception: InactiveAccount
):
    return JSONResponse(
        status_code=401, content={"message": "Not authenticated, Account isn't active"}
    )


async def missing_resource_exception_handler(
    request: Request, exception: MissingResource
):
    return JSONResponse(
        status_code=422, content={"message": "No such resource by that UUID or name"}
    )


async def missing_premission_exception_handler(
    request: Request, exception: MissingPermission
):
    return JSONResponse(
        status_code=403, content={"message": "No permissions for resource"}
    )


async def invalid_login_exception_handler(request: Request, exception: InvalidLogin):
    return JSONResponse(
        status_code=401, content={"message": "Invalid username or password"}
    )


async def bad_request_exception_handler(request: Request, exception: InvalidRequest):
    return JSONResponse(status_code=400, content={"message": "Invalid request"})


exception_handlers = {
    NotAuthenticated: not_authenticated_exception_handler,
    InvalidLogin: invalid_login_exception_handler,
    InvalidRequest: bad_request_exception_handler,
    MissingPermission: missing_premission_exception_handler,
    MissingResource: missing_resource_exception_handler,
    InactiveAccount: inactive_account_exception_handler,
    InvalidToken: invalid_token_exception_handler,
}

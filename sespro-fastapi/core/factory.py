import logging.config
import yaml
from typing import Dict, Optional, Type, Union, Callable

from fastapi import FastAPI, exception_handlers
from fastapi.staticfiles import StaticFiles
from fastapi_versioning import VersionedFastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from api.api import router
from core.config import settings
from core.error import exception_handlers
from database import create_all_tables


def version_app(
    app: FastAPI,
    exception_handlers: Optional[Dict[Union[int, Type[Exception]], Callable]],
    **kwargs
):
    app = VersionedFastAPI(
        app, root_path=app.root_path, exception_handlers=exception_handlers, **kwargs
    )

    # Hack: Register exception handlers in all mounted subapps
    # We need this workaround because fastapi-versioning is not passing them downstream to sub-apps by default
    mounted_routes = [route for route in app.routes if isinstance(route, Mount)]

    if exception_handlers is not None:
        for mounted_route in mounted_routes:
            for exc, exc_handler in exception_handlers.items():
                mounted_route.app.add_exception_handler(exc, exc_handler)

    return app


def create_app(create_tables: bool = False, check_tables: bool = True):
    app = FastAPI(title=settings.API_TITLE, root_path=settings.API_ROOT_PATH)

    create_all_tables(create_tables, check_tables)

    app.include_router(router)

    app = version_app(app, exception_handlers=exception_handlers)
    app.mount("/static", StaticFiles(directory="static"))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


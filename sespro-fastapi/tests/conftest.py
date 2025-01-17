import os
from typing import Any, Dict, Generator, List

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from database.db import db, create_all_tables
from core.config import settings

from .utils.load_data import generate_audit_json, grab_data, load_user_data
from .utils.s3_test_helper import clean_test_folder


def pytest_generate_tests(metafunc):
    os.environ['ENVIRONMENT'] = "TEST"


@pytest.fixture(scope='session')
def create_tables_load_data() -> Generator:
    create_all_tables()
    load_user_data()
    audit_data = generate_audit_json()
    yield audit_data

    db.drop_all_tables(with_all_data=True)
    clean_test_folder()


# Create a new application for testing
@pytest.fixture
def app(create_tables_load_data: None) -> FastAPI:
    from core.factory import create_app
    return create_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app,
                               base_url="http://testserver",
                               headers={"Content-Type":
                                        "application/json"}) as client:
            yield client


@pytest.fixture
async def users_data() -> List[Dict[str, Any]]:

    data = grab_data("auth.json")

    return data


@pytest.fixture()
async def exclude_pass_na():
    settings.INCLUDE_PASS = False
    settings.INCLUDE_NA = False


@pytest.fixture()
async def include_pass_na():
    settings.INCLUDE_PASS = True
    settings.INCLUDE_NA = True


@pytest.fixture()
async def exclude_pass():
    settings.INCLUDE_PASS = False
    settings.INCLUDE_NA = True


@pytest.fixture()
async def exclude_na():
    settings.INCLUDE_PASS = True
    settings.INCLUDE_NA = False


"""@pytest.fixture()
async def load_audit_data(create_tables_load_data: None) -> Dict[str, Any]:

    audit_data = generate_audit_json()
    yield audit_data
"""
from typing import Any, Dict, List

import pytest
from core.config import settings
from faker import Faker
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_400_BAD_REQUEST,
)

faker = Faker()


class TestAuthRoutes:
    @pytest.mark.asyncio
    async def test_user_creation(self, client: AsyncClient):
        user = {
            "email": faker.free_email(),
            "password": faker.pystr(max_chars=16),
            "name": faker.name(),
        }
        res = await client.post(f"{settings.API_V1_0STR}/auth/register", json=user)
        result = res.json()
        assert res.status_code == HTTP_201_CREATED
        assert result == {"registered": True}

    @pytest.mark.asyncio
    async def test_invalid_request_raises(self, client: AsyncClient):
        user = {"email": faker.free_email(), "name": faker.name()}
        res = await client.post(f"{settings.API_V1_0STR}/auth/register", json=user)

        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_users_uniquity(self, client: AsyncClient):
        user = {
            "email": faker.free_email(),
            "password": faker.pystr(max_chars=16),
            "name": faker.name(),
        }
        res = await client.post(f"{settings.API_V1_0STR}/auth/register", json=user)
        assert res.status_code == HTTP_201_CREATED

        res = await client.post(f"{settings.API_V1_0STR}/auth/register", json=user)
        assert res.status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_inactive_user_after_registration(self, client: AsyncClient):
        user = {
            "email": faker.free_email(),
            "password": faker.pystr(max_chars=16),
            "name": faker.name(),
        }
        res = await client.post(f"{settings.API_V1_0STR}/auth/register", json=user)
        result = res.json()
        assert res.status_code == HTTP_201_CREATED
        assert result == {"registered": True}

        user.pop("name", None)
        res = await client.post(f"{settings.API_V1_0STR}/auth/login", json=user)

        assert res.status_code == HTTP_401_UNAUTHORIZED
        result = res.json()
        assert result == {"message": "Not authenticated, Account isn't active"}

    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient, users_data: List[Dict[str, Any]]):
        user = users_data[0]
        user.pop("name", None)
        user.pop("active", None)

        res = await client.post(f"{settings.API_V1_0STR}/auth/login", json=user)
        result = res.json()
        assert res.status_code == HTTP_200_OK
        assert "token" in result.keys()

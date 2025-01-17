import base64
from logging import getLogger
import json
from datetime import datetime
from typing import Any, Dict

import pytest
import requests
from faker import Faker
from httpx import AsyncClient
from pony.orm import db_session
from starlette.status import HTTP_200_OK


from core.config import settings
from schema import SubmitSchema
from tests.utils.load_data import (
    grab_data,
)
from utils.helpers import save_parsed_audit, update_parsed_audit
from tests.utils.load_data import get_no_questions_in_parse_audit

faker = Faker()
logger = getLogger()


async def upload_picture_request(
    client: AsyncClient, data: Dict[str, Any], location, question
):
    image = requests.get(url="https://source.unsplash.com/random/200x200?sig=1")

    img = image.content

    data_str = base64.b64encode(img).decode("ascii")

    data = {"data": data_str}

    users_data = grab_data("auth.json")
    user_data = users_data[1]
    user_data.pop("name", None)
    user_data.pop("active", None)

    res = await client.post(f"{settings.API_V2_0STR}/auth/login", json=user_data)

    result = res.json()
    token = result["token"]

    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        f"{settings.API_V2_0STR}/audit/image/{location}/{question}",
        json=data,
        headers=headers,
    )

    return {"response": res, "headers": headers, "img": img}


class TestAuditRoutes:
    @pytest.mark.asyncio
    @db_session
    async def test_edited_parsed_questions(
        self, create_tables_load_data: Dict[str, Any]
    ):
        audit_json = create_tables_load_data["audit_json"]
        data = {
            "type": str(create_tables_load_data["user_details"]["template"]),
            "location": str(create_tables_load_data["user_details"]["premises"]),
            "stime": datetime.now(),
            "etime": datetime.now(),
            "body": json.loads(audit_json),
        }
        obj_in = SubmitSchema(**data)
        result = save_parsed_audit(
            obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
        )
        no_parsed_question_dict = get_no_questions_in_parse_audit([1])

        assert no_parsed_question_dict[f"{1}"] == 6
        assert result["success"] == True
        print(result)
        scored_audit = result["result"]["scored_audit"]

        edited_audit_json = create_tables_load_data["edited_audit_json"]
        data = {
            "type": str(create_tables_load_data["user_details"]["template"]),
            "location": str(create_tables_load_data["user_details"]["premises"]),
            "stime": datetime.now(),
            "etime": datetime.now(),
            "body": json.loads(edited_audit_json),
        }
        obj_in = SubmitSchema(**data)

        result = update_parsed_audit(
            obj_in=obj_in,
            user=create_tables_load_data["user_details"]["users"][0],
            parsed_audit=scored_audit,
        )
        assert result["success"] == True


class TestAuditUserRoutes:
    @pytest.mark.asyncio
    async def test_get_picture(
        self, client: AsyncClient, create_tables_load_data: Dict[str, Any]
    ):

        location = create_tables_load_data["user_details"]["premises"]
        question = create_tables_load_data["questions"][0]

        result = await upload_picture_request(
            client=client,
            data=create_tables_load_data,
            location=location,
            question=question,
        )
        res = result["response"]
        headers = result["headers"]
        assert res.status_code == HTTP_200_OK
        result = res.json()
        assert result["upload"] == True

        _uuid = result["uuid"]

        res = await client.get(f"{settings.API_V1_0STR}/audit/photo/{_uuid}")

        assert res.status_code == 200

        image = requests.get(url="https://source.unsplash.com/random/200x200?sig=1")

        img = image.content

        data_str = base64.b64encode(img).decode("ascii")

        data = {"data": data_str}

        res = await client.put(
            f"{settings.API_V2_0STR}/edit/photo/{_uuid}",
            json=data,
            headers=headers,
        )
        assert res.status_code == 200
        result = res.json()

        assert _uuid == result["uuid"]

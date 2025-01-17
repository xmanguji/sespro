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
    get_no_questions_in_parse_audit,
    grab_data,
    get_audits_by_premise,
    get_no_failed_questions_in_parse_audit,
)
from utils.helpers import remap, save_parsed_audit

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

    res = await client.post(f"{settings.API_V1_0STR}/auth/login", json=user_data)

    result = res.json()
    token = result["token"]

    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post(
        f"{settings.API_V1_0STR}/audit/image/{location}/{question}",
        json=data,
        headers=headers,
    )

    return {"response": res, "headers": headers, "img": img}


class TestAuditRoutes:
    @pytest.mark.asyncio
    @db_session
    async def test_parsed_questions(self, create_tables_load_data: Dict[str, Any]):
        audit_json = create_tables_load_data["audit_json"]
        data = {
            "type": str(create_tables_load_data["user_details"]["template"]),
            "location": str(create_tables_load_data["user_details"]["premises"]),
            "stime": datetime.now(),
            "etime": datetime.now(),
            "body": json.loads(audit_json),
        }
        obj_in = SubmitSchema(**data)
        save_parsed_audit(
            obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
        )
        no_parsed_question_dict = get_no_questions_in_parse_audit([1])
        assert no_parsed_question_dict[f"{1}"] == 6

    @pytest.mark.asyncio
    @db_session
    async def test_audit_query_by_location(
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
        for i in range(110):
            save_parsed_audit(
                obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
            )
        audits = get_audits_by_premise(data_obj=create_tables_load_data)
        assert len(audits) == 111


class TestAuditUserRoutes:
    @pytest.mark.asyncio
    async def test_upload_picture(
        self, client: AsyncClient, create_tables_load_data: Dict[str, Any]
    ):

        location = create_tables_load_data["user_details"]["premises"]
        question = create_tables_load_data["questions"][0]

        res = await upload_picture_request(
            client=client,
            data=create_tables_load_data,
            location=location,
            question=question,
        )
        res = res["response"]
        assert res.status_code == HTTP_200_OK
        result = res.json()
        assert result["upload"] == True

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
        assert res.status_code == HTTP_200_OK
        result = res.json()
        assert result["upload"] == True

        _uuid = result["uuid"]

        res = await client.get(f"{settings.API_V1_0STR}/audit/photo/{_uuid}")

        assert res.status_code == 200

    @pytest.mark.asyncio
    async def test_wrong_uuid_picture(self, client: AsyncClient):

        _uuid = faker.uuid4()

        res = await client.get(f"{settings.API_V1_0STR}/audit/photo/{_uuid}")

        assert res.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_picture(
        self, client: AsyncClient, create_tables_load_data: Dict[str, Any]
    ):

        location = create_tables_load_data["user_details"]["premises"]
        question = create_tables_load_data["questions"][0]

        res = await upload_picture_request(
            client=client,
            data=create_tables_load_data,
            location=location,
            question=question,
        )
        headers = res["headers"]
        res = res["response"]

        assert res.status_code == HTTP_200_OK
        result = res.json()
        assert result["upload"] == True

        _uuid = result["uuid"]

        res = await client.delete(
            f"{settings.API_V1_0STR}/audit/photo/{_uuid}", headers=headers
        )

        assert res.status_code == 200
        result = res.json()
        assert result["deleted"] == True

    @pytest.mark.asyncio
    @db_session
    async def test_include_all_questions_only(
        self, create_tables_load_data, include_pass_na
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
        saved = save_parsed_audit(
            obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
        )
        remapped = remap(
            scored_audit=saved["result"]["scored_audit"],
            user=create_tables_load_data["user_details"]["users"][0],
            obj_in=obj_in,
        )
        no_parsed_question_dict = get_no_questions_in_parse_audit([1])
        assert no_parsed_question_dict[f"{1}"] == 6
        questions = json.loads(remapped["final_remap"])["failures_for_this_audit"]
        num_questions = 0
        for category in questions:
            num_questions += len(category[1][0])
        assert num_questions == no_parsed_question_dict[f"{1}"] + 2

    @pytest.mark.asyncio
    @db_session
    async def test_false_questions_only(self, create_tables_load_data, exclude_pass_na):
        audit_json = create_tables_load_data["audit_json"]
        data = {
            "type": str(create_tables_load_data["user_details"]["template"]),
            "location": str(create_tables_load_data["user_details"]["premises"]),
            "stime": datetime.now(),
            "etime": datetime.now(),
            "body": json.loads(audit_json),
        }
        obj_in = SubmitSchema(**data)
        saved = save_parsed_audit(
            obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
        )
        print(saved)
        remapped = remap(
            scored_audit=saved["result"]["scored_audit"],
            user=create_tables_load_data["user_details"]["users"][0],
            obj_in=obj_in,
        )
        no_failed_questions = get_no_failed_questions_in_parse_audit([1])
        no_parsed_question_dict = get_no_questions_in_parse_audit([1])
        assert no_parsed_question_dict[f"{1}"] == 6
        questions = json.loads(remapped["final_remap"])["failures_for_this_audit"]
        num_questions = 0
        for category in questions:
            if category[1]:
                num_questions += len(category[1][0])
        assert num_questions == no_failed_questions

    @pytest.mark.asyncio
    @db_session
    async def test_exclude_pass_questions_only(
        self, create_tables_load_data, exclude_pass
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
        saved = save_parsed_audit(
            obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
        )
        remapped = remap(
            scored_audit=saved["result"]["scored_audit"],
            user=create_tables_load_data["user_details"]["users"][0],
            obj_in=obj_in,
        )
        no_failed_questions = get_no_failed_questions_in_parse_audit([1])
        no_parsed_question_dict = get_no_questions_in_parse_audit([1])
        assert no_parsed_question_dict[f"{1}"] == 2
        questions = json.loads(remapped["final_remap"])["failures_for_this_audit"]
        num_questions = 0
        for category in questions:
            num_questions += len(category[1][0])
        assert num_questions == no_parsed_question_dict[f"{1}"]

    @pytest.mark.asyncio
    @db_session
    async def test_exclude_skipped_questions_only(
        self, create_tables_load_data, exclude_na
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
        saved = save_parsed_audit(
            obj_in=obj_in, user=create_tables_load_data["user_details"]["users"][0]
        )
        remapped = remap(
            scored_audit=saved["result"]["scored_audit"],
            user=create_tables_load_data["user_details"]["users"][0],
            obj_in=obj_in,
        )
        no_failed_questions = get_no_failed_questions_in_parse_audit([1])
        no_parsed_question_dict = get_no_questions_in_parse_audit([1])
        assert no_parsed_question_dict[f"{1}"] == 6
        questions = json.loads(remapped["final_remap"])["failures_for_this_audit"]
        num_questions = 0
        for category in questions:
            num_questions += len(category[1][0])
        assert num_questions == 2

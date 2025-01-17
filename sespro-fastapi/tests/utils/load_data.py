from datetime import datetime
import json
from model.parsed import ParsedAudit
import random
from pathlib import Path
from utils.helpers import save_parsed_audit
from schema.utils import SubmitSchema
from typing import Any, Dict, List

from faker import Faker
from pony.orm import db_session
from pony.orm.core import TransactionIntegrityError

from core.config import settings
from crud import parsed as crud_parsed, parsed_questions as crud_questions
from model import AuditTemplate, User, Question, Category, Premises, PremisesGroup, Manager
from database import create_all_tables, db

faker = Faker()

data_dir = Path.cwd() / 'tests/data'


def generate_questions(num: int) -> List[Dict[str, Any]]:
    questions = []
    for _ in range(num):
        random_type = random.randint(1, 3)
        question = {
            "type": random_type,
            "text": faker.text(),
            "worth": random.randint(1, 5),
            "weight": random.uniform(1.0, 2.0),
            "attachments": json.dumps({})
        }
        questions.append(question)
    return questions


def grab_data(loc: str) -> List[Dict[str, Any]]:
    with open(f'{data_dir}/{loc}') as f:
        full_data = json.load(f)
    return full_data


@db_session
def load_user_data(login: bool = True):
    users_data = grab_data("auth.json")
    premise_group = grab_data("premise_group.json")
    users = []
    if login:
        user_data = users_data[0]
    else:
        user_data = users_data[1]
    manager = Manager(name=user_data["name"], email=user_data["email"])
    premise_group = PremisesGroup(**(premise_group[0]))
    loc = Premises(name=user_data["name"],
                   manager=manager,
                   group=premise_group.uuid)
    user = User(**user_data, premises=loc)
    user.set_password(password=user_data["password"])
    users.append(user)
    return {"premises": loc.uuid, "users": users, "manager": manager.uuid}


@db_session
def get_no_questions_in_parse_audit(ids: List) -> Dict[str, int]:

    data = {}
    for id in ids:
        data[f'{id}'] = len(ParsedAudit[id].questions)

    return data


@db_session
def get_no_failed_questions_in_parse_audit(ids: List) -> int:
    questions = []
    for id in ids:
        questions = questions + list(ParsedAudit[id].questions)

    reports = [question.uuid for question in questions]

    failed_questions = crud_questions.get_failed_question(
        challenge_questions=[], questions=reports)[:]
    return len(failed_questions)


@db_session
def generate_audit_json(q_num: int = 3):

    user_details = load_user_data(login=False)

    question_uuids = []
    category_uuids = []
    categories = grab_data("categories.json")

    for category in categories:
        category_obj = Category(**category)
        questions = generate_questions(q_num + 1)
        for question in questions:
            question_obj = Question(category=category_obj, **question)
            question_uuids.append(question_obj.uuid)
        category_uuids.append(category_obj.uuid)

    categories = {}
    n = 1
    for category in category_uuids:
        categories[f'{n}'] = str(category)
        n += 1
    questions = {}
    n = 1
    for question in question_uuids:
        questions[f'{n}'] = str(question)
        n += 1

    _template = AuditTemplate(name="Test Template",
                              categories=categories,
                              questions=questions)

    user_details["template"] = _template.uuid

    audit_json = _template.build_audit()

    for category in audit_json:
        x = 0
        for question in category["questions"]:
            if x == 2:
                x += 1
                question["skipped"] = True
                continue
            question["pass"] = False
            if x == 1:
                question["pass"] = True
            x += 1

    edited_audit_json = []
    for category in audit_json:
        x = 0
        for question in category["questions"]:
            if x == 2:
                x += 1
                question["skipped"] = False
                continue
            question["pass"] = True
            if x == 1:
                question["pass"] = True
            x += 1
        edited_audit_json.append(category)

    return ({
        "audit_json": json.dumps(audit_json),
        "user_details": user_details,
        "questions": question_uuids,
        "edited_audit_json": json.dumps(edited_audit_json)
    })


def test_data():
    user_details = load_user_data(login=False)
    audit_json = grab_data("data_audit.json")
    audit_json["location"] = str(user_details["premises"])

    return ({
        "audit_json": audit_json,
        "user_details": user_details,
    })


@db_session
def get_audits_by_premise(data_obj: Dict[str, Any]):

    answer = crud_parsed.get_audit(uuid=data_obj["user_details"]["premises"],
                                   first=False)
    return answer


@db_session
def test_exclude_skipped_questions_only(generate_audit_json):
    settings.INCLUDE_NA = True
    settings.INCLUDE_PASS = True
    audit_json = generate_audit_json["audit_json"]
    """data = {
        "type": str(generate_audit_json["user_details"]["template"]),
        "location": str(generate_audit_json["user_details"]["premises"]),
        "stime": datetime.now(),
        "etime": datetime.now(),
        "body": json.loads(audit_json)
    }

    obj_in = SubmitSchema(**data)"""
    obj_in = SubmitSchema(**audit_json)
    remapped = save_parsed_audit(
        obj_in=obj_in, user=generate_audit_json["user_details"]["users"][0])
    no_failed_questions = get_no_failed_questions_in_parse_audit([1])
    no_parsed_question_dict = get_no_questions_in_parse_audit([1])
    questions = (json.loads(
        remapped["result"]["final_remap"])["summed_failures_for_this_site"])
    num_questions = 0
    for category in questions:
        num_questions += len(category[1][0])


if __name__ == "__main__":
    create_all_tables()
    try:
        data = test_data()
        test_exclude_skipped_questions_only(data)

    except TransactionIntegrityError:
        db.drop_all_tables(with_all_data=True)

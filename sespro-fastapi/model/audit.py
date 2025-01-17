import json
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from uuid import UUID, uuid4

import typing
from pony.orm import PrimaryKey, Required, Json, select, Set, Optional, StrArray

from database import db


class DataError(Exception):
    pass


class QuestionType(Enum):
    BINARY = 0  # Pass or fail; notes can be submitted
    CHECK = 1  # Pass or fail; images can be submitted
    ASK = 2  # Pass or fail; note submission and questions are pooled


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()')
    text = Required(str)
    icon = Required(str)
    color = Required(str)

    audit_template_categories = Set('AuditTemplateCategory')
    questions = Set('Question')

    parsedQuestion = Set('ParsedQuestion')

    parent = Optional(UUID)
    children = Optional(StrArray)  # optional arrays are empty (not null)
    challenge = Required(bool, default=False, sql_default=False)


class Question(db.Entity):
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()')

    category = Required('Category')  # Order within audit is determined in the template
    type = Required(int)  # Use QuestionType
    text = Required(str)
    audit_template_questions = Set('AuditTemplateQuestion')
    parsedQuestions = Set('ParsedQuestion')

    worth = Required(int)
    weight = Required(float, default=1.)
    '''
    key -> val (Str)
    { help }
    '''
    attachments = Required(Json)

    def build_json(self):

        cq = {
            'uuid': str(self.uuid),
            'category': str(self.category.uuid),
            'type': self.type,
            'text': self.text,
            'order': int(question.order),
            'worth': db_q.worth
        }

        if 'hint' in db_q.attachments:
            cq['hint'] = db_q.attachments['hint']

        if 'non_applicable' in db_q.attachments:
            cq['non_applicable'] = db_q.attachments['non_applicable']

        if 'non_observable' in db_q.attachments:
            cq['non_observable'] = db_q.attachments['non_observable']

        if 'reference' in db_q.attachments:
            cq['reference'] = db_q.attachments['reference']

        if 'guide' in db_q.attachments:
            cq['hint'] = {'text': db_q.attachments['guide'], 'images': []}


class AuditTemplateQuestion(db.Entity):
    _table_ = 'audit_template_question'
    id = PrimaryKey(int, auto=True)
    question = Required(Question)
    audit_template = Required('AuditTemplate')
    order = Required(int)


class AuditTemplateCategory(db.Entity):
    _table_ = 'audit_template_category'
    id = PrimaryKey(int, auto=True)
    audit_template = Required('AuditTemplate')
    category = Required(Category)
    order = Required(int)


class AuditTemplate(db.Entity):
    _table_ = 'audit_template'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()')
    name = Required(str)
    creator = Required(UUID)
    organization = Optional(UUID)

    questions = Set('AuditTemplateQuestion')
    categories = Set('AuditTemplateCategory')

    users = Set('User', table='audit_template_users', column='user_id')

    enabled = Required(bool, default=True, sql_default='TRUE')
    date_created = Required(datetime, sql_default='CURRENT_TIMESTAMP'),

    parsed_audits = Set('ParsedAudit')

    def build_categories_json(self):

        categories = []

        category_uuids = [c.category.uuid for c in self.categories]

        for cat in self.categories:
            db_cat = cat.category
            local = cat.order
            built_cat = {
                'uuid': str(db_cat.uuid),
                'text': db_cat.text,
                'icon': db_cat.icon,
                'order': int(local),
                'questions': [],
                'color': db_cat.color
            }

            if db_cat.parent is not None and db_cat.parent in category_uuids:
                built_cat['parent'] = str(db_cat.parent)

            if len(db_cat.children) > 0:
                built_cat['children'] = db_cat.children

            if db_cat.challenge:
                built_cat['challenge'] = True

            categories.append(built_cat)

        categories.sort(key=lambda x: x["order"])

        return categories

    def build_audit(self) -> typing.List:

        audits = []

        category_uuids = [c.category.uuid for c in self.categories]

        for cat in self.categories:
            db_cat = cat.category
            local = cat.order
            built_cat = {
                'uuid': str(db_cat.uuid),
                'text': db_cat.text,
                'icon': db_cat.icon,
                'order': int(local),
                'questions': [],
                'color': db_cat.color
            }

            if db_cat.parent is not None and db_cat.parent in category_uuids:
                built_cat['parent'] = str(db_cat.parent)

            if len(db_cat.children) > 0:
                built_cat['children'] = db_cat.children

            if db_cat.challenge:
                built_cat['challenge'] = True

            questions = [q for q in self.questions if q.question in db_cat.questions]

            for question in questions:

                db_q = question.question

                cq = {
                    'uuid': str(db_q.uuid),
                    'category': str(db_cat.uuid),
                    'type': db_q.type,
                    'text': db_q.text,
                    'order': int(question.order)-1,
                    'worth': db_q.worth
                }

                if 'hint' in db_q.attachments:
                    cq['hint'] = db_q.attachments['hint']

                if 'non_applicable' in db_q.attachments:
                    cq['non_applicable'] = db_q.attachments['non_applicable']

                if 'non_observable' in db_q.attachments:
                    cq['non_observable'] = db_q.attachments['non_observable']

                if 'reference' in db_q.attachments:
                    cq['reference'] = db_q.attachments['reference']

                if 'guide' in db_q.attachments:
                    cq['hint'] = {'text': db_q.attachments['guide'], 'images': []}

                built_cat["questions"].append(cq)

            built_cat["questions"].sort(key=lambda x: x["order"])

            audits.append(built_cat)

        audits.sort(key=lambda x: x["order"])

        return audits

    def render_json(self) -> str:
        return json.dumps(self.build_audit())


class AuditInProgress(db.Entity):
    id = PrimaryKey(int, auto=True)

    user = Required('User')
    premises = Required('Premises')

    data = Required(Json)
    date_created = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    def validate_template(self, data: str) -> bool:
        try:
            json_data = json.loads(data)
            if 'type' in json_data.keys():
                if json_data['type'] == self.template.uuid:
                    return True
        except JSONDecodeError:
            return False

        return False

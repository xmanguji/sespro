from datetime import datetime
from uuid import UUID, uuid4

from pony.orm import PrimaryKey, Required, Optional, Set, Json, composite_key

from database import db
from .audit import Question, Category, AuditTemplate
from .premises import Premises


class ParsedAudit(db.Entity):
    _table_ = 'parsed_audit'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()', unique=True)

    audit_template = Required(AuditTemplate)

    premises = Required(UUID)
    user = Required(UUID)

    raw_data_key = Required(str)
    raw_data_uri = Required(str)

    images = Set('AuditImage')

    questions = Set('ParsedQuestion')

    score = Required(int, default=0)
    max_score = Required(int, default=0)
    score_percentage = Required(float, default=.0)

    final_comments = Optional(str, nullable=True)
    extra = Optional(Json, nullable=True)

    start_time = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    end_time = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    date_submitted = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    timezone = Optional(str, nullable=True)

    def build_json_result(self):

        parsed_audit = {
            'uuid': str(self.uuid),
            'type': str(self.audit_template.uuid),
            'location': str(self.premises),
            'final_comments': self.final_comments,
            'extra': self.extra,
            'stime': str(self.start_time),
            'etime': str(self.end_time),
            'body': self.audit_template.build_categories_json()
        }

        for category in parsed_audit["body"]:

            for q in self.questions:

                json_question = q.build_json_result()

                if json_question['category'] == category['uuid']:
                    category['questions'].append(json_question)

        return parsed_audit


class ParsedQuestion(db.Entity):
    _table_ = 'parsed_question'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()', unique=True)

    question = Required(Question)

    category = Required(Category)

    parsed_audit = Required(ParsedAudit)

    images = Set('AuditImage')

    worth = Required(int)
    passed = Required(bool, default=False)
    notes = Optional(str)
    # composite_key(question, parsed_audit)

    def build_json_result(self):

        question = {
            'uuid': str(self.uuid),
            'category': str(self.category.uuid),
            'type': self.question.type,
            'text': self.question.text,
            'worth': self.worth,
            'notes': self.notes,
            'pass': self.passed,
            'images': [img.image_uri for img in list(self.images)] if self.images else []
        }

        for atq in self.question.audit_template_questions:

            if atq.audit_template is self.parsed_audit.audit_template:
                question['order'] = atq.order

            return question


class AuditImage(db.Entity):
    _table_ = 'audit_image'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()', unique=True)

    user = Required(UUID)

    premises = Required(UUID)

    question = Required(UUID)

    parsed_audit = Optional(ParsedAudit)

    parsed_question = Optional(ParsedQuestion)

    image_key = Required(str)

    image_uri = Required(str)

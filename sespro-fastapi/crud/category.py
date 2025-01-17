from typing import List

from pydantic.types import UUID4
from pony.orm import select

from .base import CRUDBase
from model import Category, AuditTemplateCategory, AuditTemplate

from schema import CategoryCreate, CategoryUpdate, ReadCategory, ReadQuestion


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def get_categories(self, template_id) -> List[ReadCategory]:

        audit = AuditTemplate.get(id=template_id)

        # categories = select(c for c in Category)
        categories = [ac.category for ac in AuditTemplateCategory.select(lambda ac: ac.audit_template == audit)]

        data = []

        for category in categories:
            questions = category.questions

            question_data = [ReadQuestion(id=question.id, text=question.text, uuid=question.uuid, weight=question.weight) for question in questions]
            question_data_sorted = sorted(question_data, key=lambda q: q.id)

            category_data = ReadCategory(
                text=category.text, 
                uuid=str(category.uuid),
                id=str(category.id),
                questions=question_data_sorted,
                audit_id=template_id
            )
            data.append(category_data)

        return data


category = CRUDCategory(Category)

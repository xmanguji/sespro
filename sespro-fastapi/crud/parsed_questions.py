from typing import Any, Dict, Optional, Tuple, Union

from pony.orm import select, desc, count
from pony.orm.core import Query, QueryResult
from pydantic import UUID4

from .base import CRUDBase
from .parsed_audit import parsed as crud_parsed
from model import ParsedQuestion
from schema import ParsedQuestionCreate, ParsedQuestionUpdate


class CRUDParsedQuestion(
    CRUDBase[ParsedQuestion, ParsedQuestionCreate, ParsedQuestionUpdate]
):
    def create(
        self, *, obj_in: Union[ParsedQuestionCreate, Dict[str, Any]]
    ) -> ParsedQuestion:

        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=True)

        parsed_question = ParsedQuestion(**obj_in)

        return parsed_question

    def get_failed_question_and_count(
        self,
        *,
        challenge_questions: list,
        reports: list,
        limit: Optional[int] = None,
        sort_by: Optional[Dict] = None
    ) -> Tuple[Union[UUID4, int]]:

        pqs = select(
            (pq.uuid, count(pq))
            for pq in ParsedQuestion
            if pq.parsed_audit in reports
            and not pq.passed
            and pq.uuid not in challenge_questions
        )

        if sort_by:
            if sort_by["desc"]:
                sort_string = sort_by["sort_by"]
                pqs = pqs.sort_by(desc(sort_string))
            else:
                sort_string = sort_by["sort_by"]
                pqs = pqs.sort_by(sort_string)
        if limit:
            pqs = pqs.limit(limit)

        return pqs

    def get_failed_question(
        self,
        *,
        challenge_questions: list,
        questions: list,
        limit: Optional[int] = None,
        sort_by: Optional[Dict] = None
    ) -> Union[QueryResult, Query, Any]:

        pqs = select(
            (pq.uuid) for pq in ParsedQuestion if pq.uuid in questions and not pq.passed
        )

        if sort_by:
            if sort_by["desc"]:
                sort_string = sort_by["sort_by"]
                pqs = pqs.sort_by(desc(sort_string))
            else:
                sort_string = sort_by["sort_by"]
                pqs = pqs.sort_by(sort_string)
        if limit:
            pqs = pqs.limit(limit)

        return pqs

    def get_failed_category_and_count(
        self,
        *,
        challenge_questions: list,
        reports: list,
        limit: Optional[int] = None,
        sort_by: Optional[Dict] = None
    ) -> Tuple[Union[UUID4, int]]:

        pqs = select(
            (pq.category, count(pq))
            for pq in ParsedQuestion
            if pq.parsed_audit in reports
            and not pq.passed
            and pq.uuid not in challenge_questions
        )

        if sort_by:
            if sort_by["desc"]:
                sort_string = sort_by["sort_by"]
                pqs = pqs.sort_by(desc(sort_string))
            else:
                sort_string = sort_by["sort_by"]
                pqs = pqs.sort_by(sort_string)
        if limit:
            pqs = pqs.limit(limit)

        return pqs

    def get_by_question_and_audit(self, *, question: str, audit: str) -> Optional[ParsedQuestion]:

        parsed_question_query = ParsedQuestion.select(lambda pq : str(pq.question.uuid) == question and str(pq.parsed_audit.uuid) == audit)

        parsed_question = parsed_question_query.first()

        if parsed_question:
            return parsed_question
        else:
            return None

parsed_questions = CRUDParsedQuestion(ParsedQuestion)

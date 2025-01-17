from typing import Any, Dict, List, Optional, Union

from pony.orm import select, desc
from pydantic import UUID4

from .base import CRUDBase
from model import ParsedAudit, ParsedQuestion, AuditTemplate
from schema import ParsedAuditCreate, ParsedAuditUpdate


class CRUDParsedAudit(CRUDBase[ParsedAudit, ParsedAuditCreate, ParsedAuditUpdate]):
    def get_parsed_audits_by_template_and_premises(
        self,
        *,
        premises: UUID4,
        template: UUID4,
        group: Optional[bool] = None,
        limit: Optional[int] = None,
        sort_by: Optional[Dict] = None
    ) -> List[ParsedAudit]:

        if group:
            reports = select(
                a
                for a in ParsedAudit
                if a.premises in premises and a.audit_template.uuid == template
            )
        else:
            reports = select(
                a
                for a in ParsedAudit
                if a.premises == premises and a.audit_template.uuid == template
            )

        if sort_by:
            if sort_by["desc"]:
                sort_string = sort_by["sort_by"]
                reports = reports.sort_by(desc(sort_string))
            else:
                sort_string = sort_by["sort_by"]
                reports = reports.sort_by(sort_string)
        if limit:
            reports = reports.limit(limit)
        reports = reports[:]
        return reports

    def get_audit(
        self,
        *,
        uuid: UUID4,
        limit: Optional[int] = None,
        sort_by: Optional[Dict] = None,
        first: bool
    ) -> Union[List[ParsedAudit], ParsedAudit]:

        audits = select(a for a in ParsedAudit if a.premises == uuid)

        if sort_by:
            if sort_by["desc"]:
                sort_string = sort_by["sort_by"]
                audits = audits.sort_by(desc(sort_string))
            else:
                sort_string = sort_by["sort_by"]
                audits = audits.sort_by(sort_string)
        if limit:
            audits = audits.limit(limit)
        if first:
            audits = audits.first()

        return audits

    def update_parsed_questions(
        self, *, uuid: UUID4, obj_in: Union[ParsedAuditUpdate, Dict[str, Any]]
    ) -> ParsedAuditUpdate:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        db_obj = ParsedAudit.get(uuid=uuid)
        pq = ParsedQuestion[update_data["parsedquestion"]]
        db_obj.questions += pq

    def create(self, *, obj_in: Union[ParsedAuditCreate, Dict[str, Any]]) -> ParsedAuditCreate:
        """Create or Store new data

        Args:
            obj_in (Union[CreateSchema, Dict[str, Any]]): the data to store

        Returns:
            ModelType: [description]
        """

        obj_in['audit_template'] = AuditTemplate.get(uuid=obj_in['audit_template'])

        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data)

        return db_obj

parsed = CRUDParsedAudit(ParsedAudit)

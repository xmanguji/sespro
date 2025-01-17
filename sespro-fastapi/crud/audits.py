from typing import Any, Dict, List, Union
from fastapi.encoders import jsonable_encoder

from pony.orm import select
from pydantic.types import UUID4

from .base import CRUDBase
from model import AuditTemplate, Category, AuditImage, ParsedAudit, ParsedQuestion
from schema import (
    AuditTemplateCreate,
    AuditTemplateUpdate,
    AuditImageCreate,
    AuditInProgress,
)


class CRUDAuditTemplate(
    CRUDBase[AuditTemplate, AuditTemplateCreate, AuditTemplateUpdate]
):

    def get_category_by_uuid(self, *, uuid: UUID4) -> Category:

        c = select(c for c in Category if c.uuid == uuid).first()

        return c

    def get_image_by_uuid(self, *, uuid: UUID4):
        d_img = select(i for i in AuditImage if i.uuid == uuid).first()
        return d_img

    def remove_image(self, *, db_obj: AuditImage):
        db_obj = AuditImage.get(uuid=db_obj.uuid)
        try:
            db_obj.delete()
        except:
            return False
        return True

    def create_image(
        self, *, obj_in: Union[AuditImageCreate, Dict[str, Any]]
    ) -> AuditImage:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = jsonable_encoder(obj_in)
            if obj_in.parsed_audit:
                obj_in_data["parsed_audit"] = ParsedAudit.get(uuid=obj_in.parsed_audit)
            
            if obj_in.parsed_question:
                obj_in_data["parsed_question"] = ParsedQuestion.get(uuid=obj_in.parsed_question)

        db_obj = AuditImage(**obj_in_data)

        return db_obj

    def update_audit_image(
        self, *, obj_in: Dict[str, Any], db_obj: AuditImage
    ) -> AuditImage:
        aip = self.get_image_by_uuid(uuid=db_obj.uuid)
        aip.set(**obj_in)
        return aip

    def get_audit_progress_by_uuid(self, *, uuid) -> List[AuditInProgress]:
        db_objs = select(s for s in AuditInProgress if s.premises.uuid == uuid)[:]
        return db_objs

    def create_audit_progress(self, *, obj_in: Dict[str, Any]) -> AuditInProgress:

        db_obj = AuditInProgress(**obj_in)
        return db_obj

    def update_audit_progress(
        self, *, obj_in: Dict[str, Any], db_obj: AuditInProgress
    ) -> AuditInProgress:
        aip = self.get_audit_progress_by_uuid(db_obj.premises.uuid)
        aip.set(**obj_in)
        return aip

    def get_images_first_remap(
        self, *, user: UUID4, location: UUID4, question: UUID4
    ) -> List[AuditImage]:
        d_imgs = select(
            i
            for i in AuditImage
            if i.user == user
            and i.premises == location
            and str(i.question) == str(question)
            and not i.parsed_audit
        )[:]
        return d_imgs

    def get_images_post_remap(self, *, parsedaudit: UUID4, question: UUID4, parsed_question: str):
        d_imgs = select(
            i for i in AuditImage if str(i.parsed_audit.uuid) == str(parsedaudit) and str(i.question) == str(question) and str(i.parsed_question.uuid) == str(parsed_question)
        )[:]
        return d_imgs


audits = CRUDAuditTemplate(AuditTemplate)

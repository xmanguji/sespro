from typing import List

from pydantic.types import UUID4
from pony.orm import select

from .base import CRUDBase
from model import Role
from schema import CreateRole, UpdateRole, ReadRole


class CRUDRole(CRUDBase[Role, CreateRole, UpdateRole]):
    def get_roles(self) -> List[ReadRole]:
        roles = list(select((r.name, r.uuid, r.displayName) for r in Role))
        data = [{"name": name, "uuid": str(uuid), 'displayName': str(displayName)} for name, uuid, displayName in roles]

        return data

    def get_by_name(self, name) -> Role:

        obj = self.model.get(name=name)

        return obj

role = CRUDRole(Role)



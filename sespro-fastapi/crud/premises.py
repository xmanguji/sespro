from typing import List

from pydantic.types import UUID4
from pony.orm import select, desc

from .base import CRUDBase
from model import Premises, PremisesGroup, User, PremisesOrganization, Role
from schema import PremisesCreate, PremisesUpdate, PremisesShort, ManagerSchema, ReadPremise, ReadPremises
# from crud import user as crud_user
from pony.orm import db_session

class CRUDPremises(CRUDBase[Premises, PremisesCreate, PremisesUpdate]):
    def get_user_premises(self, user: User) -> List[PremisesShort]:

        user = User.get(uuid=user.uuid)

        premises = list(select(p for p in Premises if user in p.users).order_by((lambda: p.name)))
        # orgUUIDs = [t.uuid for t in user.premises_organization]
        # orgUUIDs = list(set(orgUUIDs))
        
        # print('====================== org UUIDs ====================', orgUUIDs)
        
        # premises = list(select(p for p in Premises if p.group.premises_organization.uuid in orgUUIDs).order_by((lambda: p.name)))
        data = [{"name": p.name, "uuid": str(p.uuid)} for p in premises]

        return data

    def get_group_list(self, obj_in: Premises, premises: bool = False) -> List[UUID4]:
        if not premises:
            group_list = select(
                p.uuid
                for p in Premises
                if p.group == obj_in.group and p.group is not None
            )[:]
            return group_list
        else:
            group_list = select(
                p for p in Premises if p.group == obj_in.group and p.group is not None
            )[:]
            return group_list

    def get_premsise_group_by_uuid(self, *, uuid: UUID4) -> PremisesGroup:

        group = select(pg for pg in PremisesGroup if str(pg.uuid) == str(uuid)).first()
        
        return group

    def get_manager_details(self, *, uuid: UUID4) -> ManagerSchema:

        location = Premises.get(uuid=uuid)

        user = select(u for u in location.group.users if u.role.name == 'ROLE_MANAGER').first() if location is not None else select(p for p in User if p.role.name == 'ROLE_ROOT').first()

        if user is not None:
            manager = ManagerSchema(
                uuid=user.uuid, email=user.email, name=user.name
            ) 
        else:
            manager = None

        return manager


    def get_group_manager(self, *, uuid: str) -> ManagerSchema:

        group = PremisesGroup.get(uuid=uuid)

        user = select(u for u in group.users if u.role.name == 'ROLE_MANAGER' or u.role.name == 'ROLE_ROOT').first() if group is not None else None
        
        if user is not None:
            manager = ManagerSchema(
                uuid=user.uuid, email=user.email, name=user.name
            ) 
        else:
            manager = None

        return manager
    
    def get_premises(self, user: User, sort: str = 'asc') -> List[ReadPremise]:
        user = User.get(uuid=user.uuid)

        role_name = Role[user.role.id]
        if role_name.name == 'ROLE_ROOT':
            premises = list(select(p for p in Premises).order_by((lambda: p.name) if sort == 'asc' else (lambda: desc(p.name))))
            data = [
                {
                     "name": str(p.name), 
                     "uuid": str(p.uuid),
                     "group": str(p.group.name) if p.group is not None else "",
                     "group_uuid": str(p.group.uuid) if p.group is not None else ""
                } for p in premises]

        elif role_name.name == 'ROLE_OWNER':
            
            orgUUIDs = [t.uuid for t in user.premises_organization]
            orgUUIDs = list(set(orgUUIDs))
            premises = list(select(p for p in Premises if p.group.premises_organization.uuid in orgUUIDs).order_by((lambda: p.name) if sort == 'asc' else (lambda: desc(p.name))))
            data = [
                {
                    "name": str(p.name), 
                    "uuid": str(p.uuid),
                    "group": str(p.group.name) if p.group is not None else "",
                    "group_uuid": str(p.group.uuid) if p.group is not None else "",
                    'organization': str(p.group.premises_organization.name) if p.group is not None else "",
                    # g.premises_organization.name if g.premises_organization is not None else ''
                } for p in premises]
        else:
            uPremises = user.premises
            userGroupPremises = user.premises_group.premises

            premises = uPremises + list(set(userGroupPremises) - set(uPremises))

            data = [
                {
                    "name": str(p.name), 
                    "uuid": str(p.uuid),
                    "group": str(p.group.name) if p.group is not None else "",
                    "group_uuid": str(p.group.uuid) if p.group is not None else ""} for p in premises]

        return data

    def get_groups(self, user: User, sort: str = 'asc') -> List[PremisesGroup]:
        user = User.get(uuid=user.uuid)

        role_name = Role[user.role.id]
        if role_name.name == 'ROLE_ROOT':
            groups = list(select(g for g in PremisesGroup).order_by((lambda: g.name) if sort == 'asc' else (lambda: desc(g.name))))
        else:
            orgUUIDs = [t.uuid for t in user.premises_organization]
            orgUUIDs = list(set(orgUUIDs))
            groups = list(select(g for g in PremisesGroup if g.premises_organization.uuid in orgUUIDs).order_by((lambda: g.name) if sort == 'asc' else (lambda: desc(g.name))))
        return groups

    def get_organizations(self, user: User, sort: str = 'asc') -> List[PremisesOrganization]:
        
        role_name = Role[user.role.id]
        if role_name.name == 'ROLE_ROOT':
            organizations = list(select(o for o in PremisesOrganization).order_by((lambda: o.name) if sort == 'asc' else (lambda: desc(o.name))))
        else:
            organizations = list(select(o for o in PremisesOrganization if user in o.users).order_by((lambda: o.name) if sort == 'asc' else (lambda: desc(o.name))))
        return organizations


premises = CRUDPremises(Premises)

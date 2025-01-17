from typing import List

from pydantic.types import UUID4
from pony.orm import select

from .base import CRUDBase
from model import AuditTemplate, User, PremisesOrganization, Role
from schema import CreateTemplate, UpdateTemplate, ReadTemplate, Template
from uuid import UUID


class CRUDTemplate(CRUDBase[AuditTemplate, CreateTemplate, UpdateTemplate]):
    def get_templates(self, user: User) -> List[ReadTemplate]:

        user = User.get(uuid=user.uuid)
        role_name = Role[user.role.id]
                
        orgUUIDs = [t.uuid for t in user.premises_organization]
        orgUUIDs = list(set(orgUUIDs))
        
        templateUUIDs = [t.uuid for t in user.templates]
        templateUUIDs = list(set(templateUUIDs))
        
        premises = list(select((p.name, p.uuid, p.id, p.creator, p.organization) for p in AuditTemplate).order_by(lambda: p.name))

        # if(role_name.name == 'ROLE_ROOT'): 

        data = []
        for name, uuid, id, creator, organization in premises:
            
            creatorObject = User.get(uuid=creator)
            organizationObject = PremisesOrganization.get(uuid=organization)
            
            if organizationObject is not None :
                root_org = {
                    "name": organizationObject.name,
                    "uuid": organizationObject.uuid
                }
            else: 
                root_org = {
                    "name": '',
                    "uuid": ''
                }

            if creatorObject is not None :
                role_creator = Role[creatorObject.role.id]

                if creatorObject.premises_organization and role_creator.name != 'ROLE_ROOT': 
                    
                    ttt = [{'uuid': str(org.uuid), 'name': str(org.name)} for org in creatorObject.premises_organization]

                    org = {
                        "uuid": ttt[0]['uuid'],
                        "name": ttt[0]['name'],
                    }
                else: 
                    org = {
                        "uuid": None,
                        "name": None,
                    }
                creator_data = {
                    "name": creatorObject.name,
                    "uuid": creatorObject.uuid,
                    "org": org
                }
            else: 
                creator_data = {
                    "name": None,
                    "uuid": None,
                    "org": {
                        "uuid": None,
                        "name": None,
                    }
                }

            template_data = {
                "name": name,
                "uuid": str(uuid),
                "id": id,
                "creator": creator_data,
                "organization": root_org,
            }
            
            if(role_name.name == 'ROLE_ROOT'): 
                data.append(template_data)
                
            else:
                if (creator_data["org"]["uuid"] is not None and UUID(creator_data["org"]["uuid"]) in orgUUIDs) or organization in orgUUIDs :
                # if organization in orgUUIDs :
                    if(role_name.name == 'ROLE_OWNER'): 
                        data.append(template_data)
                    else:
                        if(uuid in templateUUIDs):
                            data.append(template_data)

        return data
        
        # data = [
        #     {
        #         "name": name, 
        #         "uuid": str(uuid), 
        #         "id": id,
        #         "creator": {
        #             "name": creator.name,
        #             "uuid": creator.uuid,
        #         }
        #     } for name, uuid, id, creator in premises]

        # return data

templates = CRUDTemplate(AuditTemplate)

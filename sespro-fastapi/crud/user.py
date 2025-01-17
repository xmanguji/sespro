from pony.orm.core import commit
from pydantic.main import BaseModel
from pydantic.types import UUID4
import crud
from typing import Any, Dict, Optional, Union, List

from model import ControlToken, User
from pony.orm import select, desc
from schema import RegisterFull, RegisterOut, UserUpdate, ReadUser, ReadUsers, ControlToken as Schema_CT, templates

from .base import CRUDBase
from .manager import manager as crud_manager
from .premises import premises as crud_premises


class RegisteredData(BaseModel):
    user: RegisterOut
    token: Schema_CT


class CRUDUser(CRUDBase[User, RegisterFull, UserUpdate]):
    def create_token(self, *, obj_in: Union[Schema_CT, Dict[str, Any]]) -> ControlToken:

        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_none=True)

        t = ControlToken(**(obj_in_data))

        return t

    def create(
        self, *, obj_in: Union[RegisterFull, Dict[str, Any]], google_reg: bool = False
    ) -> Union[User, RegisteredData]:
        """[summary]

        Args:
            obj_in (Union[RegisterFull, Dict[str, Any]]): User
            google_reg (bool, optional): Google OAuth. Defaults to False.

        Returns:
            Union[User, RegisteredData]: The User Model (Entity)
        """

        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_none=True)

        if not google_reg:
            password = obj_in["password"]
            obj_in_data["password"] = "PREHASH"
            obj_in_data["active"] = False

        else:
            obj_in_data["password"] = "GOOGLE"

        user = User(
            **obj_in_data,
        )


        loc = crud_premises.create(obj_in={"name": obj_in["name"]})
        user.premises += loc

        if google_reg:
            commit()
            return user

        self.update_password(db_obj=user, password=password)
        t = self.create_token(obj_in={"user": user.uuid})

        commit()

        out_data = RegisteredData(user=user.to_dict(), token=t.to_dict())

        return out_data

    def create_new_user(
        self, *, obj_in: Union[RegisterFull, Dict[str, Any]]
    ) -> Union[User, RegisteredData]:
        """[summary]

        Args:
            obj_in (Union[RegisterFull, Dict[str, Any]]): User
            google_reg (bool, optional): Google OAuth. Defaults to False.

        Returns:
            Union[User, RegisteredData]: The User Model (Entity)
        """

        password = obj_in["password"]

        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_none=True)


        user = User(
            **obj_in_data,
        )

        t = self.create_token(obj_in={"user": user.uuid})

        commit()

        if password != '':
            self.update_password(db_obj=user, password=password)

        out_data = RegisteredData(user=user.to_dict(), token=t.to_dict())

        return out_data


    def get_by_email(self, *, email: str) -> User:
        """Get a user by the user email

        Args:
            email (str): the user email

        Returns:
            User: the user object
        """

        obj = self.model.get(email=email)

        return obj

    def get_token(
        self, *, token: Optional[str] = None, uuid: Optional[str] = None
    ) -> Union[ControlToken, bool]:
        """Find user activation Token

        Args:
            token (Optional[str], optional): [description]. Defaults to None.
            uuid (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Union[ReturnControlToken, bool]: Returns False if such token doesn't exists, Returns data if it does
        """
        t = None
        if token:
            t = select(t for t in ControlToken if t.token == token).first()
        elif uuid:
            t = select(t for t in ControlToken if t.user == uuid).first()

        if t is None:
            return False

        return t

    def update_password(self, *, db_obj: User, password: str) -> bool:
        """Update Password

        Args:
            db_obj (User): [description]
            password (str): [description]

        Returns:
            bool: [description]
        """
        db_obj = self.get_by_uuid(uuid=db_obj.uuid)
        db_obj.set_password(password=password)
        return True

    def delete_verification_token(self, *, t: ControlToken) -> bool:
        """Delete already verified Token

        Args:
            t (ControlToken): The ControlToken db obj

        Returns:
            bool: True
        """

        t = select(t for t in ControlToken if t.token == t.token).first()
        t.delete()
        return True

    def activate_account(self, uuid: UUID4) -> bool:
        """Activate user account

        Returns:
            bool: True or False
        """
        user = self.get_by_uuid(uuid=uuid)
        if not user:
            return False

        user.active = True
        return True

    # def get_users(self, sort: str = 'asc') -> List[User]:
    #     users = list(select(u for u in User for t in u.templates for p in u.premises).order_by((lambda: u.name) if sort == 'asc' else (lambda: desc(u.name))))

    #     data = [
    #         {
    #             'uuid': str(u.uuid), 
    #             'name': str(u.name), 
    #             'email': u.email, 
    #             'role': str(u.role.displayName) if u.role is not None else '', 
    #             'isActive': u.active,
    #             'templates': [{'uuid': str(t.uuid), 'name': str(t.name)} for t in list(u.templates)],
    #             'premises': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in list(u.premises)],
    #             'premises_group': {'uuid': str(u.premises_group.uuid), 'name': str(u.premises_group.name)},
    #             'premises_organization': {'uuid': str(u.premises_organization.uuid), 'name': str(u.premises_organization.name)}
    #             } 
    #             for u in users]

    #     return data
    def get_users(self, sort: str = 'asc') -> List[User]:
        users = select(u for u in User for t in u.templates for p in u.premises).distinct().order_by((lambda: u.name) if sort == 'asc' else (lambda: desc(u.name)))[:]
        
        return list(users)

    def get_user_details(self, uuid: UUID4) -> User:

        user_info = select(u for u in User if str(u.uuid) == str(uuid)).first()

        user_details = {
            'uuid': str(user_info.uuid),
            'name': str(user_info.name),
            'email': str(user_info.email),
            'role': {
                'name': str(user_info.role.name),
                'displayName': str(user_info.role.displayName),
                'uuid': str(user_info.role.uuid)
            },
            'isActive': user_info.active,
            'templates': [{'uuid': str(t.uuid), 'name': str(t.name)} for t in user_info.templates],
            'premises': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in user_info.premises],
            'premises_group': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in user_info.premises_group],
            'premises_organization': [{'uuid': str(p.uuid), 'name': str(p.name)} for p in user_info.premises_organization]
        }

        return user_details

    def hasAdminRole(self, uuid: str) -> bool:
        user = self.get_by_uuid(uuid=uuid)
        return user.role.name == 'ROLE_ROOT' or user.role.name == 'ROLE_MANAGER'


user = CRUDUser(User)

import hashlib
from datetime import datetime
from uuid import UUID, uuid4

import bcrypt as bcrypt
from pony.orm import Required, PrimaryKey, Set, Optional

from database import db


class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, unique=True, sql_default='uuid_generate_v4()', default=uuid4)
    name = Required(str, unique=True)
    displayName = Optional(str)
    order = Required(int)
    users = Set('User')


class User(db.Entity):
    _table_ = 'users'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()')

    name = Required(str)
    email = Required(str, unique=True)
    password = Required(str)

    premises = Set('Premises', table='premises_users', column='premises_id')
    templates = Set('AuditTemplate', table='audit_template_users', column='audit_template_id')

    audits_in_progress = Set('AuditInProgress')

    active = Required(bool, default=True, sql_default=True)
    date_created = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    role = Required(Role)
    premises_group = Set('PremisesGroup', table='premises_group_users', column='group_id')
    premises_organization = Set('PremisesOrganization', table='premises_organization_users', column='organization_id')

    def set_password(self, password: str):
        password = password.encode('utf8')
        self.password = bcrypt.hashpw(password,
                                      bcrypt.gensalt(12)).decode('utf8')

    def check_password(self, user_password: str) -> bool:
        user_password = user_password.encode('utf8')
        return bcrypt.checkpw(user_password, self.password.encode('utf-8'))

    def get_password(self):
        return self.password.encode('utf-8')

    def add_premises(self, premises: db.Entity):
        self.premises.add(premises)

    def add_groups(self, premises_group: db.Entity):
        self.premises_groups.add(premises_group)

    def add_organizations(self, premises_organization: db.Entity):
        self.premises_groups.add(premises_organization)


class Manager(db.Entity):
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()')

    name = Required(str)
    email = Required(str, unique=True)


class ControlToken(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(UUID)
    token = Required(str,
                     default=lambda: hashlib.sha224(
                         str(uuid4()).encode('utf8')).hexdigest())

    date_created = Required(datetime, sql_default='CURRENT_TIMESTAMP')

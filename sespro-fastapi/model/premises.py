from datetime import datetime
from uuid import UUID, uuid4

from pony.orm import PrimaryKey, Required, Set, Optional

from database import db


class Premises(db.Entity):
    _table_ = 'premises'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()')

    name = Required(str)

    users = Set('User', table='premises_users', column='user_id')

    group = Optional('PremisesGroup')

    audits_in_progress = Set('AuditInProgress')

    date_created = Required(datetime, sql_default='CURRENT_TIMESTAMP')


class PremisesGroup(db.Entity):
    _table_ = 'premises_group'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()', unique=True)
    name = Required(str)
    render_enabled = Required(bool, default=True, sql_default=True)
    premises_organization = Optional('PremisesOrganization')
    premises = Set(Premises)
    users = Set('User', table='premises_group_users', column='user_id')


class PremisesOrganization(db.Entity):
    _table_ = 'premises_organization'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()', unique=True)
    name = Required(str)
    render_enabled = Required(bool, default=True, sql_default=True)
    premises_groups = Set(PremisesGroup)
    users = Set('User',  table='premises_organization_users', column='user_id')


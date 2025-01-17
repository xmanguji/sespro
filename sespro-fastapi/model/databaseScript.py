import typing
import json
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from uuid import UUID, uuid4
from pony.orm import PrimaryKey, Required, Json, select, Set, Optional, StrArray
from database import db


class DatabaseScript(db.Entity):
    _table_ = 'database_script'
    id = PrimaryKey(int, auto=True)
    uuid = Required(UUID, default=uuid4, sql_default='uuid_generate_v4()', unique=True)
    scriptName = Required(str, unique=True, column='script_name')
    hash = Required(str)


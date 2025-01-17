from core.config import settings
from pony import orm

db = orm.Database()

db.bind(**settings.DB_DICT)


def db_instance():
    return db


def create_all_tables(create_tables, check_tables):
    db.generate_mapping(create_tables=create_tables, check_tables=check_tables)
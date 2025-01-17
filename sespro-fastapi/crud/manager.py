from .base import CRUDBase
from model.user import Manager
from schema import ManagerCreate, ManagerUpdate


class CRUDManager(CRUDBase[Manager, ManagerCreate, ManagerUpdate]):

    pass


manager = CRUDManager(Manager)
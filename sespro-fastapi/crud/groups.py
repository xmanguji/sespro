from .base import CRUDBase
from model import PremisesGroup
from schema import ReadPremisesOrganization, CreatePremisesGroup, UpdatePremisesGroup


class CRUDPremisesGroup(CRUDBase[PremisesGroup, CreatePremisesGroup, UpdatePremisesGroup]):
    pass


group = CRUDPremisesGroup(PremisesGroup)

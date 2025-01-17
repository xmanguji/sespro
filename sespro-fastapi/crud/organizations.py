from .base import CRUDBase
from model import PremisesOrganization
from schema import ReadPremisesOrganization, CreatePremisesOrganization, UpdatePremisesOrganization


class CRUDPremisesOrganization(CRUDBase[PremisesOrganization, CreatePremisesOrganization, UpdatePremisesOrganization]):
    pass


organization = CRUDPremisesOrganization(PremisesOrganization)

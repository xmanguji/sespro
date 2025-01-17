from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class BaseOut(BaseModel):
    id: Optional[int]
    date_created: Optional[datetime]


class BaseOutUuid(BaseOut):
    uuid: UUID4


class BaseOutName(BaseOut):
    name: str

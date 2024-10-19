from pydantic import BaseModel, UUID4
from typing import Optional, List

from app.schemas.service_schema import ServiceSchema
from app.schemas.windows_schema import WindowSchema


class OfficeBase(BaseModel):
    name: str
    address: str


class OfficeCreate(OfficeBase):
    pass


class OfficeSchema(OfficeBase):
    id: UUID4
    services: List[ServiceSchema] = []
    windows: List[WindowSchema] = []

    class Config:
        from_attributes = True

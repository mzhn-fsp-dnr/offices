from typing import List
from pydantic import UUID4, BaseModel
from . import service_schema


class WindowBase(BaseModel):
    name: str


class WindowCreate(WindowBase):
    pass


class WindowSchema(WindowBase):
    id: UUID4
    services: List[service_schema.ServiceSchema] = []

    class Config:
        from_attributes = True

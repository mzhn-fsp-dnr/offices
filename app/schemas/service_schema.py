from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import Optional, List


class ServiceBase(BaseModel):
    name: str
    parent_id: Optional[UUID]

    def as_dict(self):
        return {
            "name": self.name,
            "parent_id": None if self.parent_id is None else str(self.parent_id),
        }


class ServiceCreate(ServiceBase):
    pass


class ServiceSchema(ServiceBase):
    id: UUID
    children: List["ServiceSchema"] = []

    class Config:
        from_attributes = True


class ServiceWindowLink(BaseModel):
    service_id: UUID4
    window_id: UUID4

    class Config:
        from_attributes = True


class ServiceWindowUnlink(BaseModel):
    service_id: UUID4

    class Config:
        from_attributes = True

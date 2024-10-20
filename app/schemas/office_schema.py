from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional, List

from app.schemas.service_schema import ServiceSchema
from app.schemas.windows_schema import WindowSchema


class OfficeBase(BaseModel):
    name: str
    address: str
    week_days: List[int]
    start_time: str
    end_time: str

    def as_dict(self):
        return {
            "name": self.name.strip(),
            "address": self.address.strip(),
            "week_days": ",".join([str(day) for day in self.week_days]),
            "start_time": self.start_time.strip(),
            "end_time": self.end_time.strip(),
        }


class OfficeCreate(OfficeBase):
    pass


class OfficeSchema(OfficeBase):
    id: UUID4
    services: List[ServiceSchema] = []
    windows: List[WindowSchema] = []

    def as_dict(self):
        d = super(self).as_dict()
        d["id"] = self.id
        d["services"] = self.services
        d["windows"] = self.windows
        return d

    class Config:
        from_attributes = True

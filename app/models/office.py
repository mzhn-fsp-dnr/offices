import uuid
import datetime
from app.models.base import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import relationship


class OfficeModel(Base):
    __tablename__ = "offices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False, unique=True)

    week_days = Column(String, unique=False, default="0,1,2,3,4")
    start_time = Column(String, unique=False, nullable=False)
    end_time = Column(String, unique=False, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    services = relationship("OfficeService", back_populates="office")
    windows = relationship("OfficeWindow", back_populates="office")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "week_days": [day for day in self.week_days.split(",")],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "address": self.address,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class OfficeService(Base):
    __tablename__ = "office_services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    office_id = Column(UUID(as_uuid=True), ForeignKey("offices.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    office = relationship("OfficeModel", back_populates="services")

    __table_args__ = (
        Index(
            "idx_office_service_unique",
            office_id,
            service_id,
            unique=True,
        ),
    )


class OfficeEmployees(Base):
    __tablename__ = "office_employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    office_id = Column(UUID(as_uuid=True), ForeignKey("offices.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index(
            "idx_office_users_unique",
            office_id,
            user_id,
            unique=True,
        ),
    )


class OfficeWindow(Base):
    __tablename__ = "office_windows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    office_id = Column(UUID(as_uuid=True), ForeignKey("offices.id"), nullable=False)
    window_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    office = relationship("OfficeModel", back_populates="windows")

    __table_args__ = (
        Index(
            "idx_office_window_unique",
            office_id,
            window_id,
            unique=True,
        ),
    )

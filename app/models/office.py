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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    services = relationship("OfficeService", back_populates="office")
    windows = relationship("OfficeWindow", back_populates="office")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
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

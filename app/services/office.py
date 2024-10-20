from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.office_schema import OfficeCreate, OfficeSchema
from app.models.office import OfficeModel, OfficeWindow
from typing import List

from app.schemas.service_schema import ServiceCreate, ServiceSchema
from app.schemas.windows_schema import WindowCreate, WindowSchema
from app.services import services as services_service
from app.services import windows as windows_service
from app.models.office import OfficeService


def get(db: Session, id: str) -> OfficeModel:
    return db.query(OfficeModel).filter(OfficeModel.id == id).first()


def get_all(db: Session) -> List[OfficeModel]:
    return db.query(OfficeModel).all()


def create(db: Session, office: OfficeCreate):
    new_office = OfficeModel(**office.as_dict())
    db.add(new_office)
    db.commit()
    db.refresh(new_office)
    return new_office


def delete(db: Session, id: str):
    office = get(db, id)
    if office:
        db.delete(office)
        db.commit()

    return office


def update(db: Session, id: str, window: OfficeSchema):
    office = get(db, id)
    if office:
        office.name = window.name
        db.add(office)
        db.commit()

    return office


def has_service(db: Session, office_id: str, service_id: str) -> OfficeModel | None:
    res = (
        db.query(OfficeModel)
        .join(OfficeService)
        .filter(
            OfficeModel.id == office_id,
            OfficeModel.services.any(OfficeService.service_id == service_id),
        )
        .first()
    )
    return res


def link_service_to_office(db: Session, office_id: str, service: ServiceSchema):
    office = get(db, office_id)
    if not office:
        return office

    svc = OfficeService(office_id=office_id, service_id=service.id)
    office.services.append(svc)
    db.add(office)
    db.commit()
    db.refresh(office)
    return office


def link_window_to_office(db: Session, office_id: str, window: WindowSchema):
    office = get(db, office_id)
    if not office:
        return office

    win = OfficeWindow(office_id=office_id, window_id=window.id)
    office.windows.append(win)
    db.add(office)
    db.commit()
    db.refresh(office)
    return office


def link_service_to_window_on_office(
    db: Session, office_id: str, window_id: str, service_id: str
):
    office = has_service(db, office_id, service_id)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")

    windows_service.link(window_id, service_id)

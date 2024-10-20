from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import office_schema, service_schema, windows_schema
import app.services.office as office_service
import app.services.services as services_service
import app.services.windows as windows_service
from uuid import UUID

router = APIRouter(prefix="/offices")


# Create office
@router.post("/")
def create_office(
    office: office_schema.OfficeCreate, db_session: Session = Depends(get_db)
):
    return office_service.create(db_session, office).as_dict()


@router.delete("/{id}")
def delete_office(id: UUID, db_session: Session = Depends(get_db)):
    found = office_service.delete(db_session, id)
    if not found:
        raise HTTPException(status_code=404, detail="Офис не найден")

    return found


@router.get("/{id}", response_model=office_schema.OfficeSchema)
def get_office(id: UUID, db_session: Session = Depends(get_db)):

    office = office_service.get(db_session, id)
    if not office:
        raise HTTPException(status_code=404, detail="Офис не найдено")

    services = []
    for wc in office.services:
        svc = services_service.get(wc.service_id)
        if svc.parent_id == None:
            services.append(svc)

    windows = []
    for wc in office.windows:
        win = windows_service.get(wc.window_id)
        windows.append(win)

    wc = office.as_dict()
    wc["services"] = services
    wc["windows"] = windows
    return wc


@router.get("/")
def get_offices(db_session: Session = Depends(get_db)):
    offices = office_service.get_all(db_session)
    return {"items": [o.as_dict() for o in offices], "count": len(offices)}


@router.put("/{id}")
def update_window(
    id: UUID, office: office_schema.OfficeBase, db_session: Session = Depends(get_db)
):
    offfice = office_service.get(db_session, id)
    if not offfice:
        raise HTTPException(status_code=404, detail="Office не найден")

    return office_service.update(db_session, id, office)


@router.post("/{id}/service")
def create_service(
    id: UUID,
    new_service: service_schema.ServiceCreate,
    db_session: Session = Depends(get_db),
):

    service = services_service.create(new_service)
    if not service:
        raise HTTPException(status_code=400, detail="Не удалось создать услугу")

    office = office_service.link_service_to_office(db_session, id, service)
    if not office:
        raise HTTPException(status_code=404, detail="Офис не найден")

    return office


@router.post("/{id}/window")
def create_window(
    id: UUID,
    new_window: windows_schema.WindowCreate,
    db_session: Session = Depends(get_db),
):

    window = windows_service.create(new_window)
    if not window:
        raise HTTPException(status_code=401, detail="Не удалось создать окно")

    office = office_service.link_window_to_office(db_session, id, window)
    if not office:
        raise HTTPException(status_code=404, detail="Офис не найден")

    return window


@router.post("/{id}/link")
def link_service_to_window_on_office(
    id: UUID,
    body: service_schema.ServiceWindowLink,
    db_session: Session = Depends(get_db),
):
    office = office_service.get(db_session, id)
    if not office:
        raise HTTPException(status_code=404, detail="Офис не найден")

    window = windows_service.get(body.window_id)
    if not window:
        raise HTTPException(status_code=404, detail="Окно не найдено")

    service = services_service.get(body.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    office_service.link_service_to_window_on_office(
        db_session, id, window.id, service.id
    )

    return office_service.get(db_session, id)


@router.post("/{id}/unlink")
def unlink_service_from_window_on_office(
    id: UUID,
    body: service_schema.ServiceWindowUnlink,
    db_session: Session = Depends(get_db),
):
    office = office_service.get(db_session, id)
    if not office:
        raise HTTPException(status_code=404, detail="Офис не найден")

    service = services_service.get(body.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    office_service.unlink_service_from_office(db_session, office.id, service.id)

    return office_service.get(db_session, id)


@router.post("/{id}/unlink/{window_id}/{service_id}")
def unlink_service_from_window(
    id: UUID,
    window_id: UUID,
    service_id: UUID,
    db_session: Session = Depends(get_db),
):
    office = office_service.get(db_session, id)
    if not office:
        raise HTTPException(status_code=404, detail="Офис не найден")

    window = windows_service.get(window_id)
    if not window:
        raise HTTPException(status_code=404, detail="Окно не найдено")

    service = services_service.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    office_service.unlink_service_from_window_on_office(
        office.id,
        window.id,
        service.id,
    )

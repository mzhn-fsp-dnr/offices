from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import office
from app.models.base import Base
from app.db.session import engine
from app.core.config import conf_settings

Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf_settings.ALLOWED_ORIGINS,
        allow_credentials=conf_settings.ALLOW_CREDENTIALS,
        allow_methods=conf_settings.ALLOW_METHODS,
        allow_headers=conf_settings.ALLOW_HEADERS,
    )

    app.include_router(office.router)
    return app


app = get_application()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import conf_settings 

engine = create_engine(conf_settings.database_link())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        
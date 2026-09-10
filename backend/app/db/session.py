from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


if settings.database_url:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
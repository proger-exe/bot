from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sentinelmod.config import settings

engine = create_async_engine(settings.postgres_dsn, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    """Base class for all models."""
    pass

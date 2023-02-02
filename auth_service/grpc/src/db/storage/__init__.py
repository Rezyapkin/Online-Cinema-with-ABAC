from contextlib import asynccontextmanager
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.storage.base import BaseAsyncCrudStorage

engine: AsyncEngine | None = None
session_maker: sessionmaker | None = None


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Relational SQL storage Provider."""
    try:
        db = session_maker()
        logger.debug("Generated alchemy session...")
        yield db
    finally:
        await db.close()
        logger.debug("Closed alchemy session...")

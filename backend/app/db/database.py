import logging
import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from typing import AsyncGenerator

from app.core.config import settings


logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("nido").setLevel(logging.INFO)
logger = logging.getLogger("nido")


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

class AsyncDatabase:
    _instance = None
    _lock = asyncio.Lock()
    _engine = None
    _session_factory = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, pool_config=None):
        async with self._lock:
            if self._engine is None:
                # Default configuration for main FastAPI app
                default_config = {
                    'pool_size': 5,
                    'max_overflow': 3,
                    'pool_timeout': 30,
                    'pool_recycle': 1800,
                    'pool_pre_ping': True,
                }

                # Use provided config or default
                config = pool_config or default_config

                self._engine = create_async_engine(
                    SQLALCHEMY_DATABASE_URL,
                    **config,
                    echo=False
                )
                # Set up monitoring for the engine
                # await _setup_db_monitoring(self._engine)
                
                self._session_factory = sessionmaker(
                    bind=self._engine,
                    class_=AsyncSession,
                    expire_on_commit=False
                )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._engine is None:
            await self.initialize()
        
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    async def cleanup(self):
        """Cleanup database connections"""
        if self._engine:
            try:
                await self._engine.dispose()
            except RuntimeError as e:
                if "Event loop is closed" not in str(e):
                    raise
            finally:
                self._engine = None

class SyncDatabase:
    _instance = None
    _lock = asyncio.Lock()
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self):
        async with self._lock:
            if self._engine is None:
                self._engine = create_engine(
                    SQLALCHEMY_DATABASE_URL.replace('postgresql+asyncpg', 'postgresql'),
                    pool_size=2,
                    max_overflow=3,
                    pool_timeout=30,
                    pool_recycle=1800,
                    pool_pre_ping=True,
                )

    def cleanup(self):
        if self._engine:
            self._engine.dispose()
            self._engine = None

# Create global instances
db = AsyncDatabase()
# sync_db = SyncDatabase()

# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db.session() as session:
        yield session
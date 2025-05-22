from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# from psycopg_pool import AsyncConnectionPool
# from psycopg.rows import dict_row

from .api.api import api_router
from .db.database import db
from .core.config import settings

import logging

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("sweval").setLevel(logging.INFO)
logger = logging.getLogger("sweval")

class AppManager:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def create_tables(self):
        """Create all tables in the database"""
        await db.initialize()

    async def initialize_services(self):
        """Initialize all database services"""
        try:
            await db.initialize()
            logger.info("Database services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise

    async def cleanup(self):
        """Cleanup all services"""
        await db.cleanup()

app_manager = AppManager()

        
# Create the FastAPI app first
app = FastAPI(
    title=settings.PROJECT_NAME, 
    redirect_slashes=False, 
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

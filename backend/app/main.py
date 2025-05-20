from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# from psycopg_pool import AsyncConnectionPool
# from psycopg.rows import dict_row

from .api.api import api_router
# from .db.database import db, vector_store, redis_store
from .core.config import settings

import logging

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("sweval").setLevel(logging.INFO)
logger = logging.getLogger("sweval")

# class AppManager:
#     _instance = None
#     _lock = asyncio.Lock()
#     _checkpointer_pool = None
#     _checkpointer = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#         return cls._instance

#     async def create_tables(self):
#         """Create all tables in the database"""
#         await db.initialize()
#         await vector_store.create_tables()

#     async def initialize_services(self):
#         """Initialize all database services"""
#         try:
#             await db.initialize()
#             await redis_store.initialize()
#             await vector_store.initialize()
#             logger.info("Database services initialized successfully")
#         except Exception as e:
#             logger.error(f"Failed to initialize services: {e}")
#             raise

#     async def setup_checkpointer(self):
#             """Run setup for checkpointer to initialize database tables"""
#             try:
#                 logger.info("Setting up checkpointer tables...")
#                 await self.checkpointer.setup()
#                 logger.info("Checkpointer setup completed successfully")
#             except Exception as e:
#                 logger.error(f"Failed to setup checkpointer: {e}")
#                 raise    
             
#     async def initialize_checkpointer(self):
#         """Initialize the checkpointer with connection pool"""
#         async with self._lock:
#             if self._checkpointer_pool is None:
#                 try:
#                     psycopg_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
                    
#                     connection_kwargs = {
#                         "autocommit": True,
#                         "prepare_threshold": 0,
#                         "row_factory": dict_row,
#                         "connect_timeout": 10,
#                         "keepalives": 1,
#                         "keepalives_idle": 30,
#                         "keepalives_interval": 10,
#                         "keepalives_count": 5
#                     }

#                     # Create the pool without opening it in the constructor
#                     self._checkpointer_pool = AsyncConnectionPool(
#                         conninfo=psycopg_url,
#                         min_size=1,
#                         max_size=3,
#                         timeout=30.0,
#                         max_waiting=10,
#                         max_lifetime=1800,
#                         num_workers=2,
#                         kwargs=connection_kwargs,
#                         open=False  # Explicitly set open=False to avoid the warning
#                     )
#                     # Open the pool separately
#                     await self._checkpointer_pool.open()
                    
#                     # Create the checkpointer with the pool
#                     self._checkpointer = AsyncPostgresSaver(conn=self._checkpointer_pool)
#                     logger.info("Checkpointer initialized successfully")
#                 except Exception as e:
#                     logger.error(f"Failed to initialize checkpointer: {e}")
#                     raise

#     @property
#     def checkpointer(self):
#         return self._checkpointer

#     async def cleanup(self):
#         """Cleanup all services"""
#         await db.cleanup()
#         await redis_store.cleanup()
        
#         if self._checkpointer_pool:
#             await self._checkpointer_pool.close()
#             self._checkpointer_pool = None
#             self._checkpointer = None

# app_manager = AppManager()

        
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

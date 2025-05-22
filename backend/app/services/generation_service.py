import uuid 
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.schemas.api import APIResponse
from app.db.database import db
from app.core.error_handlers import AppException, NotFoundError, ForbiddenError


logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("generation_service").setLevel(logging.INFO)
logger = logging.getLogger("generation_service")

class GenerationException:
    """Base exception classes for generation operations"""
    class UploadError(AppException):
        def __init__(self, message: str = "Error processing generation upload"):
            super().__init__(status_code=400, detail=message)

    class TimeoutError(AppException):
        def __init__(self):
            super().__init__(status_code=408, detail="Operation timed out. Please try again.")

    class ResourceNotFound(NotFoundError):
        def __init__(self):
            super().__init__(f"Generation not found")

class GenerationService:
    """Service class for handling generation operations"""
    
    def __init__(self):
        self.db = db

    async def create_generation(self, generation: GenerationCreate, current_user: User) -> APIResponse:
        """Create generation with profile and vector store entry"""
        async with self.db.session() as session:
            async with session.begin():
                try:
                    pass
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Database error creating generation: {str(e)}")
                    raise AppException(status_code=500, detail=f"Database error: {str(e)}")
        return APIResponse(success=True, message="Generation created successfully")
    
    async def get_generation(self, generation_id: str, current_user: Union[User, str], include: Optional[List[str]] = None) -> APIResponse:
        """Get single account with all related data"""
        async with self.db.session() as session:
            try:
                pass
                return APIResponse(
                    success=True,
                    message="Account fetched successfully",
                    data=account_data
                )
            except NotFoundError:
                raise
            except Exception as e:
                logger.error(f"Error fetching account: {str(e)}")
                raise AppException(status_code=500, detail=str(e))
    
    async def get_generations(
        self,
        current_user: User,
        sort: str = "recent",
        order: str = "desc",
        page: int = 1,
        page_size: int = 50,
        filters: Optional[dict] = None,
        include: Optional[List[str]] = None
    ) -> APIResponse:
        """Get paginated accounts with filtering and sorting"""
        # Generate cache key based on parameters

        async with self.db.session() as session:
            try:
                pass

                return APIResponse(
                    success=True,
                    message="Accounts fetched successfully",
                    data=account_data
                )
            except Exception as e:
                logger.error(f"Error fetching accounts: {str(e)}")
                raise AppException(status_code=500, detail=str(e))

    async def update_generation(
        self, 
        generation_id: str, 
        generation_update: GenerationUpdate, 
        current_user: User
    ) -> APIResponse:
        """Update account details"""
        try:
            async with self.db.session() as session:
                async with session.begin():
                    pass
                    return APIResponse(
                        success=True,
                        message="Account updated successfully",
                        # data=account_data
                    )
        except Exception as e:
            logger.error(f"Error updating account: {str(e)}")
            raise AppException(status_code=500, detail=str(e))

    async def delete_generation(self, generation_id: str, current_user: User) -> APIResponse:
        """Delete generation and related data"""
        async with self.db.session() as session:
            async with session.begin():
                try:
                    pass
                    return APIResponse(success=True, message="Account deleted successfully")
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Error deleting account: {str(e)}")
                    raise AppException(status_code=500, detail=str(e))


# Global service instance
generation_service = GenerationService() 
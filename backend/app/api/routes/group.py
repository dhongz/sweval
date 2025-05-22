from typing import List, Optional
from fastapi import APIRouter, Depends

from app.schemas.content import ContentBase
from app.core.error_handlers import handle_exceptions, AppException
from app.schemas.api import APIResponse
from app.services.content_gen import generate_content

import logging

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("generate_api").setLevel(logging.INFO)
logger = logging.getLogger("generate_api")
router = APIRouter()

# Generate routes
@router.post("", response_model=APIResponse[str])
@handle_exceptions
async def init_group(
    content: ContentBase, 
):
    """Generate a new content"""
    try:
        group = await init_group.acall(topic=content.topic, content_type=content.content_type)
        logger.info(f"Content generated successfully: {group}")
        return APIResponse(success=True, message="Content generated successfully", data=group.content)
    except Exception as e:
        raise AppException(status_code=500, detail=str(e))

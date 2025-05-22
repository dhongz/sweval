import traceback
import json
import logging
from pydantic import BaseModel
from typing import Callable, Any, Dict, Union
from functools import wraps

from fastapi import HTTPException
from fastapi.responses import StreamingResponse, Response

from app.schemas.api import APIResponse


logger = logging.getLogger(__name__)

class AppException(HTTPException):
    """Base exception class for application errors"""
    def __init__(self, status_code: int, detail: str, errors: dict = None):
        super().__init__(status_code=status_code, detail=detail)
        self.errors = errors

class NotFoundError(AppException):
    def __init__(self, resource: str):
        super().__init__(
            status_code=404,
            detail=f"{resource} not found"
        )

class DuplicateError(AppException):
    def __init__(self, resource: str):
        super().__init__(
            status_code=409,
            detail=f"{resource} already exists"
        )

class ForbiddenError(AppException):
    def __init__(self, message: str = "You don't have permission to perform this action"):
        super().__init__(
            status_code=403,
            detail=message
        )

def handle_exceptions(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            
            # If it's a streaming response or Response object, return it directly
            if isinstance(response, (StreamingResponse, Response)):
                return response
                
            # If response is already an APIResponse, return it directly
            if isinstance(response, APIResponse):
                return response
                
            # If response is a Pydantic model, wrap it in APIResponse
            if isinstance(response, BaseModel):
                return APIResponse(
                    success=True,
                    message="Success",
                    data=response.model_dump()
                )
                
            # For all other responses, wrap them in APIResponse
            return APIResponse(
                success=True,
                message="Success",
                data=response
            )
            
        except AppException as e:
            logger.error(f"Application error in {func.__name__}: {str(e.detail)}")
            return APIResponse(
                success=False,
                message=str(e.detail),
                status=e.status_code,
                errors=getattr(e, 'errors', None)
            )
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # For streaming endpoints, yield an error event
            if getattr(func, '__name__', '') == 'stream_chat':
                async def error_stream():
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
                return StreamingResponse(
                    error_stream(),
                    media_type='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/event-stream',
                    }
                )
            
            # For regular endpoints, return error response
            return APIResponse(
                success=False,
                message=str(e),
                data=None,
                status=500
            )
            
    return wrapper
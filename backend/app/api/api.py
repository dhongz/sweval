from fastapi import APIRouter
from .routes import generation

api_router = APIRouter()


api_router.include_router(generation.router, prefix="/generate", tags=["generate"])

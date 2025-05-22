from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class ContentBase(BaseModel):
    """Base account fields shared across schemas"""
    topic: str
    content_type: str
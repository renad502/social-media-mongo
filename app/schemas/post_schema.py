from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PostCreate(BaseModel):
    content: str
    media_urls: Optional[List[str]] = []
    visibility: str = "public"


class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_urls: Optional[List[str]] = None
    visibility: Optional[str] = None


class PostResponse(BaseModel):
    id: str
    author_id: str
    content: str
    media_urls: List[str]
    visibility: str
    created_at: datetime
    updated_at: datetime

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)

class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    id: str
    post_id: str
    author_id: str
    content: str
    created_at: datetime
